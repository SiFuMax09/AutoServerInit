import paramiko
import os

class SSHClient:
    def __init__(self, logger):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.logger = logger
        self.sftp = None

    def connect(self, hostname, port, username, password=None, identity_file=None, timeout=None):
        connect_params = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'timeout': timeout,
        }

        if identity_file:
            private_key = paramiko.RSAKey.from_private_key_file(identity_file)
            connect_params['pkey'] = private_key
        else:
            connect_params['password'] = password

        self.ssh.connect(**connect_params)

    def setup_ssh_directory(self):
        self.ssh.exec_command('mkdir -p ~/.ssh && chmod 700 ~/.ssh')

    def add_public_keys(self, pubkeys_file):
        if not os.path.exists(pubkeys_file):
            self.logger.log(f"Error: The file {pubkeys_file} does not exist.")
            return False

        with open(pubkeys_file, 'r') as f:
            new_keys = set(line.strip() for line in f if line.strip())

        if not new_keys:
            self.logger.log("Error: The pubkeys file is empty.")
            return False

        self.sftp = self.ssh.open_sftp()
        remote_authorized_keys_path = '.ssh/authorized_keys'

        try:
            existing_keys = self._get_existing_keys(remote_authorized_keys_path)
            keys_to_add = new_keys - existing_keys

            if keys_to_add:
                self._append_new_keys(remote_authorized_keys_path, keys_to_add)
                self.logger.log("New public keys have been added.")
            else:
                self.logger.log("No new keys to add. All keys are already present.")

            self.ssh.exec_command('chmod 600 ~/.ssh/authorized_keys')
            return True

        finally:
            if self.sftp:
                self.sftp.close()

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    def close(self):
        if self.ssh:
            self.ssh.close()

    def _get_existing_keys(self, remote_path):
        try:
            with self.sftp.file(remote_path, 'r') as remote_file:
                return set(line.strip() for line in remote_file if line.strip())
        except IOError:
            return set()

    def _append_new_keys(self, remote_path, keys):
        with self.sftp.file(remote_path, 'a') as authorized_keys_file:
            for key in keys:
                authorized_keys_file.write(key + '\n') 