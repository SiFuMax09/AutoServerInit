import os
import sys
import shutil
import winreg
import site
import subprocess
from pathlib import Path

def add_to_path(directory):
    """Add a directory to the user's PATH environment variable."""
    try:
        # Get the current PATH
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
        try:
            path, _ = winreg.QueryValueEx(key, "PATH")
        except WindowsError:
            path = ""

        # Add our directory if it's not already there
        if directory.lower() not in [x.lower() for x in path.split(os.pathsep)]:
            new_path = f"{path}{os.pathsep}{directory}" if path else directory
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
            os.environ["PATH"] = new_path
            return True
    except WindowsError as e:
        print(f"Warning: Could not add to PATH: {e}")
    finally:
        try:
            winreg.CloseKey(key)
        except:
            pass
    return False

def get_scripts_directory():
    """Get the correct Scripts directory for installation."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a virtual environment
        return os.path.join(sys.prefix, 'Scripts')
    else:
        # We're in a user installation
        return os.path.join(site.getuserbase(), 'Scripts')

def enable_long_paths():
    """Enable long path support in Windows."""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\FileSystem",
                            0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.SetValueEx(key, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False

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
        # Get the correct Scripts directory
        scripts_dir = get_scripts_directory()
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

        # Add Scripts directory to PATH if needed
        if add_to_path(scripts_dir):
            print(f"Added {scripts_dir} to PATH")
        else:
            print(f"Note: You may need to add {scripts_dir} to your PATH manually")

        print(f"CLI command installed successfully in: {scripts_dir}")
        print("You may need to restart your terminal to use the 'serverinit' command")
        return True

    except Exception as e:
        print(f"Error installing CLI command: {e}")
        return False

def install_package():
    """Install the package using pip."""
    try:
        # First, upgrade pip to latest version
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install PyQt6 separately first
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyQt6>=6.6.1'])
        
        # Then install our package
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '.'])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing package: {e}")
        print("\nTroubleshooting steps:")
        print("1. Try running the installer with administrator privileges")
        print("2. Make sure you have the latest pip version")
        print("3. If the error persists, try installing PyQt6 manually:")
        print("   pip install PyQt6>=6.6.1")
        print("4. Then run the installer again")
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
    
    # Try to enable long paths support
    if enable_long_paths():
        print("Long path support enabled successfully.")
    else:
        print("Warning: Could not enable long path support. You may need to:")
        print("1. Run this installer as administrator")
        print("2. Enable long path support manually in Windows settings")
        print("3. Or use a shorter installation path")
    
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
    print("\nInstalling dependencies and package...")
    if install_package():
        print("Package installed successfully.")
    else:
        print("\nAlternative installation method:")
        print("1. Open a new command prompt as administrator")
        print("2. Run: pip install PyQt6>=6.6.1")
        print("3. Then run this installer again")
        return
    
    # Install CLI command
    if install_cli_command():
        print("\nImportant: You may need to restart your terminal to use the 'serverinit' command")
        print(f"The command is installed in: {get_scripts_directory()}")
    else:
        print("Failed to install CLI command.")
        return
    
    print("\nInstallation completed successfully!")
    print(f"Your public keys are stored in: {os.path.join(appdata_path, 'pubkeys')}")
    print("\nTo use the tool:")
    print("1. Open a new terminal window")
    print("2. Type 'serverinit' to start the GUI")
    print("3. Or use 'serverinit -h' to see CLI options")

if __name__ == '__main__':
    main() 