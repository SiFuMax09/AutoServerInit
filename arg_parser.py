import argparse

def setup_argument_parser():
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
    
    return parser.parse_args() 