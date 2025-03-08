# AutoServerInit

A modern tool for automated server initialization with SSH key management. Available both as a GUI and CLI tool.

## Features

- **User-Friendly GUI**
  - Modern, intuitive user interface
  - Real-time status updates and progress bars
  - File browser for SSH keys and identity files
  - Clear grouping of settings

- **Powerful CLI**
  - Full command-line support
  - Automatable processes
  - Verbose mode for detailed output
  - Dry-run option for safe testing

- **SSH Key Management**
  - Automatic public key management
  - Secure storage in AppData directory
  - Duplicate prevention
  - Automatic permission setting

- **Security Features**
  - Password or key-based authentication
  - Secure default permissions
  - Encrypted connections
  - Timeout settings

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AutoServerInit.git
cd AutoServerInit
```

2. Run the installer:
```bash
python installer.py
```

The installer:
- Creates the necessary directory structure
- Sets up the AppData directory
- Installs all dependencies
- Registers the `serverinit` command

## Usage

### GUI Mode

Start the graphical interface with:
```bash
serverinit
```

The GUI offers:
- Server connection settings
- Authentication options
- Additional configuration options
- Real-time status updates

### CLI Mode

Basic usage:
```bash
serverinit -ip SERVER_IP -u USERNAME [-p PASSWORD | -i IDENTITY_FILE]
```

Important parameters:
- `-ip`: Target server IP address
- `-u, --user`: Username (default: root)
- `-p`: SSH password
- `-i, --identity-file`: Path to private key file
- `--pubkeys`: Path to public keys file
- `-c, --command`: Additional command to execute after initialization
- `-v, --verbose`: Detailed output
- `--dry-run`: Simulation without changes
- `-t, --timeout`: Connection timeout in seconds

## Configuration

### Public Keys

Public keys are stored by default in the following directory:
```
%APPDATA%\AutoServerInit\pubkeys
```

Public keys file format:
```
# One key per line
ssh-rsa AAAAB3NzaC1... user@host
ssh-ed25519 AAAAC3... user@host
```

## System Requirements

- Python 3.6 or higher
- Windows 10/11
- Internet connection for dependency installation

## Dependencies

- paramiko >= 3.4.0 (SSH connections)
- PyQt6 >= 6.6.1 (GUI)

## Development

The project uses a modular structure:
- `main.py`: Main entry point
- `gui.py`: GUI implementation
- `ssh_client.py`: SSH connection logic
- `logger.py`: Logging functionality
- `arg_parser.py`: Command-line arguments

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For questions or issues:
1. Check the [Issues](https://github.com/yourusername/AutoServerInit/issues)
2. Create a new issue
3. Contact the developers

## Changelog

### Version 1.0.0
- Initial release with GUI and CLI
- AppData integration for public keys
- Modern, user-friendly interface
- Complete SSH key management
- Installer for easy setup
