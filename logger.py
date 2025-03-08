class Logger:
    def __init__(self, log_file=None):
        self.log_file = open(log_file, 'w') if log_file else None

    def log(self, message):
        print(message)
        if self.log_file:
            self.log_file.write(message + '\n')

    def close(self):
        if self.log_file:
            self.log_file.close() 