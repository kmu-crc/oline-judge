import os

from .utils import safety_file_write, safety_file_open
from .execution import Execution


class Compile(Execution):
    def __init__(self):
        super().__init__()

    def __call__(self, extension, path, command, code, is_checker=False):
        file_name = 'main.{}'.format(extension)

        safety_file_write(file_name, code)

        command = command.replace('code_files', file_name)
        command = [path] + command.split(',')

        result, _, _ = self.execute(command)

        if os.path.getsize('error.err'):
            result = 'C'

        return True if result == 'S' else False
