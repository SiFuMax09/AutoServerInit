import getpass
import sys
from arg_parser import setup_argument_parser
from logger import Logger
from ssh_client import SSHClient

def main():
    args = setup_argument_parser()

    # Setup password
    if args.ask_pass:
        password = getpass.getpass(prompt='SSH Password: ')
    else:
        password = args.p

    if not password and not args.identity_file:
        print("Error: You must provide a password with -p or --ask-pass, or specify an identity file with -i.")
        sys.exit(1)

    # Initialize logger
    logger = Logger(args.log)

    if args.verbose:
        logger.log(f"Connecting to {args.ip}:{args.port} as {args.user}...")

    if args.dry_run:
        logger.log("Dry run enabled. No changes will be made.")
        return

    try:
        # Initialize SSH client
        ssh_client = SSHClient(logger)

        # Connect to server
        ssh_client.connect(
            hostname=args.ip,
            port=args.port,
            username=args.user,
            password=password,
            identity_file=args.identity_file,
            timeout=args.timeout
        )

        if args.verbose:
            logger.log("Connected successfully.")

        # Setup SSH directory and add keys
        ssh_client.setup_ssh_directory()
        if args.verbose:
            logger.log(".ssh directory checked/created.")

        ssh_client.add_public_keys(args.pubkeys)

        # Execute additional command if provided
        if args.command:
            output, error = ssh_client.execute_command(args.command)
            if args.verbose:
                logger.log("Command output:")
                logger.log(output)
                if error:
                    logger.log("Command error:")
                    logger.log(error)

    except Exception as e:
        logger.log(f"Error: {e}")

    finally:
        if 'ssh_client' in locals():
            ssh_client.close()
            if args.verbose:
                logger.log("Connection closed.")
        logger.close()

if __name__ == '__main__':
    main()