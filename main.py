import argparse
import paramiko
import os

def main():
    parser = argparse.ArgumentParser(description='Connect to a server via SSH and add public keys.')
    parser.add_argument('-ip', required=True, help='IP address of the server')
    parser.add_argument('-p', required=True, help='Password for SSH authentication')
    parser.add_argument('-u', '--user', default='root', help='Username for SSH authentication (default: root)')
    parser.add_argument('--pubkeys', default='pubkeys', help='Path to the pubkeys file (default: ./pubkeys)')
    args = parser.parse_args()

    ip = args.ip
    password = args.p
    username = args.user
    pubkeys_file = args.pubkeys

    try:
        # Read public keys from the file
        if not os.path.exists(pubkeys_file):
            print(f"The file {pubkeys_file} does not exist.")
            return

        with open(pubkeys_file, 'r') as f:
            pubkeys = f.read()

        if not pubkeys.strip():
            print("The pubkeys file is empty.")
            return

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Establish the connection
        print(f"Connecting to {ip} as {username}...")
        ssh.connect(hostname=ip, username=username, password=password)
        print("Connected successfully.")

        # Check and create the .ssh directory
        ssh.exec_command('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
        print(".ssh directory checked/created.")

        # Add public keys to authorized_keys
        sftp = ssh.open_sftp()
        try:
            remote_authorized_keys = '.ssh/authorized_keys'

            # Check if the file exists
            try:
                sftp.stat(remote_authorized_keys)
                # File exists, append to it
                mode = 'a'
            except IOError:
                # File does not exist, create it
                mode = 'w'

            with sftp.file(remote_authorized_keys, mode) as authorized_keys:
                authorized_keys.write(pubkeys)
                print("Public keys have been added.")

            # Set permissions
            ssh.exec_command('chmod 600 ~/.ssh/authorized_keys')
            print("Permissions for authorized_keys set.")

        finally:
            sftp.close()

        # Close the connection
        ssh.close()
        print("Connection closed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()