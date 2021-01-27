import os
import re
import errno
import signal
import subprocess

from functools import wraps
from ptrace.binding import ptrace_traceme, ptrace_syscall, ptrace_kill


TIME_LIMIT = 5


def timeout(seconds=1, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

class Execution(object):
    def __init__(self):
        pass

    def execute(self, command, limit_time=2000, is_program=False,
                limit_memory=512, input_file='input.txt'):
        # MB -> KB
        limit_memory *= 1000

        pid = os.fork()
        if pid == 0:
            ptrace_traceme()
            os.nice(19)

            redirection_error = os.open('error.err', os.O_RDWR | os.O_CREAT | os.O_TRUNC)
            os.dup2(redirection_error, 2)

            if is_program:
                redirection_stdout = os.open('output.txt', os.O_RDWR | os.O_CREAT | os.O_TRUNC)
                os.dup2(redirection_stdout, 1)

                redirection_stdin = os.open(input_file, os.O_RDONLY)
                os.dup2(redirection_stdin, 0)

            os.execv(command[0], tuple(command[1:]))

        else:
            result, time, memory = self.trace_pid(pid, is_program, limit_time, limit_memory)
            return result, time, memory

    @timeout(2000)
    def trace_pid(self, pid, is_program, limit_time, limit_memory):
        mem_size = 0
        while True:
            wpid, status, res = os.wait4(pid, 0)
            exitCode = os.WEXITSTATUS(status)

            if res[0] >= limit_time:
                return 'T', res[0], mem_size
            if mem_size >= limit_memory:
                return 'M', res[0], mem_size

            if os.WIFEXITED(status):  # normal termination
                return 'S', res[0], mem_size

            if (exitCode is not 5) and (exitCode is not 0) and (exitCode is not 17):
                return 'R', 0, 0

            if os.WIFSIGNALED(status):
                try:
                    ptrace_kill(pid)
                except Exception as e:
                    pass

                return 'R', 0, 0

            if is_program:
                mem = subprocess.check_output('pmap {} | grep total'.format(wpid), shell=True)
                mem = mem.decode('utf-8')
                mem = int(re.findall('[0-9]+', mem)[0])
                mem_size = max(mem_size, mem)

            ptrace_syscall(wpid, 0)
