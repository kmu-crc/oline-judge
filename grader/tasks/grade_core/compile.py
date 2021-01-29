import os

from .utils import safety_file_write, safety_file_open
from .execution import Execution


class Compile(Execution):
    def __init__(self):
        super().__init__()

    def __call__(self, extension, path, command, code, file_name=[], is_checker=False):
        if type(code) == list:
            for i in range(len(code)):
                safety_file_write(file_name[i], code[i])
        else:
            file_name = ['main.{}'.format(extension)]
            safety_file_write(file_name[0], code)

        command = command.replace('code_files', ','.join(file_name))
        command = [path] + command.split(',')

        result, _, _ = self.execute(command)

        if os.path.getsize('error.err'):
            result = 'C'

        return True if result == 'S' else False
