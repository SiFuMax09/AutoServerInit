import os
import sys
import shutil
import winreg
import site
import subprocess
from pathlib import Path

def get_appdata_path():
    """Get the AppData path for storing configuration files."""
    return os.path.join(os.getenv('APPDATA'), 'AutoServerInit')

def create_appdata_directory():
    """Create the AppData directory if it doesn't exist."""
    appdata_path = get_appdata_path()
    os.makedirs(appdata_path, exist_ok=True)
    pubkeys_path = os.path.join(appdata_path, 'pubkeys')
    
    # Create default pubkeys file if it doesn't exist
    if not os.path.exists(pubkeys_path):
        with open(pubkeys_path, 'w') as f:
            f.write("# Add your public keys here, one per line\n")
    
    return appdata_path

def install_cli_command():
    """Install the CLI command to make it available system-wide."""
    try:
        # Get the Python Scripts directory
        scripts_dir = site.getusersitepackages().replace('site-packages', 'Scripts')
        os.makedirs(scripts_dir, exist_ok=True)

        # Create the CLI script
        cli_script = os.path.join(scripts_dir, 'serverinit.py')
        with open(cli_script, 'w') as f:
            f.write('''#!/usr/bin/env python
import sys
from autoserverinit.main import main

if __name__ == "__main__":
    main()
''')

        # Create the batch file for Windows
        batch_file = os.path.join(scripts_dir, 'serverinit.bat')
        with open(batch_file, 'w') as f:
            f.write(f'@echo off\n"{sys.executable}" "{cli_script}" %*')

        print(f"CLI command installed successfully. You can now use 'serverinit' from the command line.")
        return True

    except Exception as e:
        print(f"Error installing CLI command: {e}")
        return False

def install_package():
    """Install the package using pip."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '.'])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing package: {e}")
        return False

def create_setup_py():
    """Create setup.py file for package installation."""
    with open('setup.py', 'w') as f:
        f.write('''from setuptools import setup, find_packages

setup(
    name="autoserverinit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "paramiko>=3.4.0",
        "PyQt6>=6.6.1",
    ],
    entry_points={
        'console_scripts': [
            'serverinit=autoserverinit.main:main',
        ],
    },
    python_requires=">=3.6",
)
''')

def create_package_structure():
    """Create the package structure."""
    # Create package directory
    os.makedirs('autoserverinit', exist_ok=True)
    
    # Move existing files into package
    files_to_move = ['main.py', 'gui.py', 'ssh_client.py', 'logger.py', 'arg_parser.py']
    for file in files_to_move:
        if os.path.exists(file):
            shutil.move(file, os.path.join('autoserverinit', file))
    
    # Create __init__.py
    with open(os.path.join('autoserverinit', '__init__.py'), 'w') as f:
        f.write('# AutoServerInit package\n')

def main():
    print("Installing AutoServerInit...")
    
    # Create AppData directory and move pubkeys
    appdata_path = create_appdata_directory()
    print(f"Configuration directory created at: {appdata_path}")
    
    # Create package structure
    create_package_structure()
    print("Package structure created.")
    
    # Create setup.py
    create_setup_py()
    print("Setup file created.")
    
    # Install package
    if install_package():
        print("Package installed successfully.")
    else:
        print("Failed to install package.")
        return
    
    # Install CLI command
    if install_cli_command():
        print("CLI command installed successfully.")
    else:
        print("Failed to install CLI command.")
        return
    
    print("\nInstallation completed successfully!")
    print("You can now use 'serverinit' from the command line.")
    print(f"Your public keys are stored in: {os.path.join(appdata_path, 'pubkeys')}")

if __name__ == '__main__':
    main() 