import argparse
import paramiko
import os
import getpass
import sys

def main():
    parser = argparse.ArgumentParser(description='Connect to a server via SSH and add public keys.')
    parser.add_argument('-ip', required=True, help='IP address of the server')
    parser.add_argument('-p', help='Password for SSH authentication')
    parser.add_argument('--ask-pass', action='store_true', help='Prompt for password')
    parser.add_argument('-u', '--user', default='root', help='Username for SSH authentication (default: root)')
    parser.add_argument('--port', type=int, default=22, help='SSH port number (default: 22)')
    parser.add_argument('--pubkeys', default='pubkeys', help='Path to the pubkeys file (default: ./pubkeys)')
    parser.add_argument('-c', '--command', help='Command to execute on the remote server after adding keys')
    parser.add_argument('-i', '--identity-file', help='SSH private key file for authentication')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-t', '--timeout', type=int, help='SSH connection timeout in seconds')
    parser.add_argument('--dry-run', action='store_true', help='Simulate the script without making changes')
    parser.add_argument('--log', help='Path to log file')
    args = parser.parse_args()

    ip = args.ip
    username = args.user
    port = args.port
    pubkeys_file = args.pubkeys
    command = args.command
    identity_file = args.identity_file
    verbose = args.verbose
    timeout = args.timeout
    dry_run = args.dry_run
    log_file = args.log

    if args.ask_pass:
        password = getpass.getpass(prompt='SSH Password: ')
    else:
        password = args.p

    if not password and not identity_file:
        print("Error: You must provide a password with -p or --ask-pass, or specify an identity file with -i.")
        sys.exit(1)

    if log_file:
        log = open(log_file, 'w')
    else:
        log = None

    def log_print(message):
        print(message)
        if log:
            log.write(message + '\n')

    if verbose:
        log_print(f"Connecting to {ip}:{port} as {username}...")

    if dry_run:
        log_print("Dry run enabled. No changes will be made.")
        return

    try:
        # Read public keys from the local pubkeys file
        if not os.path.exists(pubkeys_file):
            log_print(f"Error: The file {pubkeys_file} does not exist.")
            return

        with open(pubkeys_file, 'r') as f:
            new_keys = set(line.strip() for line in f if line.strip())

        if not new_keys:
            log_print("Error: The pubkeys file is empty.")
            return

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connection parameters
        connect_params = {
            'hostname': ip,
            'port': port,
            'username': username,
            'timeout': timeout,
        }

        # Authenticate using password or private key
        if identity_file:
            private_key = paramiko.RSAKey.from_private_key_file(identity_file)
            connect_params['pkey'] = private_key
        else:
            connect_params['password'] = password

        ssh.connect(**connect_params)

        if verbose:
            log_print("Connected successfully.")

        # Check and create the .ssh directory
        ssh.exec_command('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
        if verbose:
            log_print(".ssh directory checked/created.")

        # Open SFTP session
        sftp = ssh.open_sftp()
        try:
            remote_authorized_keys_path = '.ssh/authorized_keys'

            # Read existing authorized_keys from the remote server
            try:
                with sftp.file(remote_authorized_keys_path, 'r') as remote_file:
                    existing_keys = set(line.strip() for line in remote_file if line.strip())
            except IOError:
                # If the authorized_keys file does not exist, start with empty set
                existing_keys = set()

            # Determine which keys need to be added
            keys_to_add = new_keys - existing_keys

            if keys_to_add:
                # Append the new keys to authorized_keys
                with sftp.file(remote_authorized_keys_path, 'a') as authorized_keys_file:
                    for key in keys_to_add:
                        authorized_keys_file.write(key + '\n')
                log_print("New public keys have been added.")
            else:
                log_print("No new keys to add. All keys are already present.")

            # Set permissions
            ssh.exec_command('chmod 600 ~/.ssh/authorized_keys')
            if verbose:
                log_print("Permissions for authorized_keys set.")

        finally:
            sftp.close()

        # Execute additional command if provided
        if command:
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if verbose:
                log_print("Command output:")
                log_print(output)
                if error:
                    log_print("Command error:")
                    log_print(error)

        # Close the connection
        ssh.close()
        if verbose:
            log_print("Connection closed.")

    except Exception as e:
        log_print(f"Error: {e}")

    finally:
        if log:
            log.close()

if __name__ == '__main__':
    main()