import os
import re
import random

from .utils import safety_file_open, safety_file_write
from .message import SOLUTION_FAIL, CHECK_FAIL, SEVER_ERROR, PROBLEM_ERROR
from .execution import Execution


class Grade(Execution):
    def __init__(self, time, memory, problem_type):
        super().__init__()
        self.time = time
        self.memory = memory
        self.problem_type = problem_type
        self.total_time = 0
        self.total_memory = 0

    def __call__(self, grading_info):
        if self.problem_type == 'F':
            return self.grade_follow_problem(grading_info['submit_code'], grading_info['testcase'])
        else:
            return self.grade_problem(grading_info)


    def grade_follow_problem(self, code, testcase):
        code = code.split('\n')
        ans = testcase[0][1].split('\n')
        result = self.check_output(code, ans, True)
        return ('S', 0, 0, '') if result else ('F', 0, 0, '')

    def grade_problem(self, grading_info, testcase_size=10):
        command = self.make_command(grading_info['run_path'], grading_info['run_command'])
        if self.problem_type == 'C':
            checker_command = self.make_command(grading_info['checker__language__run_path'],
                                                grading_info['checker__language__run_command'].replace('main', 'checker'))
        else:
            checker_command = ''

        output_file_name = 'output.txt'
        input_file_name = '{}.in'.format(random.randrange(100, 1000))

        # run submit code < enter input testcase
        testcase_cnt = 0
        skip_size = (len(grading_info['testcase']) // testcase_size)
        skip_size = skip_size if skip_size > 1 else skip_size + 1
        for idx in range(0, len(grading_info['testcase']), skip_size):
            testcase_cnt += 1
            case = grading_info['testcase'][idx]

            safety_file_write(input_file_name, case[0])
            result, time, memory = self.execute(command, self.time, True, self.memory, input_file_name)

            if result == 'R':
                return result, time, memory, safety_file_open('error.err')
            elif result != 'S':
                return result, time, memory, ''

            self.total_time += time
            self.total_memory += memory

            if self.problem_type == 'C':
                # run checker program
                # checker program uses the output of submit code as input
                checker_result, _, _ = self.execute(output_file_name, checker_command)
                if checker_result != 'S':
                    return 'P', 0, 0, PROBLEM_ERROR.format('CHECKER 코드 런타임 에러')

            success, output = safety_file_open(output_file_name)

            if success:
                if (self.problem_type == 'S') and (not self.check_output(output, case[1].split('\n'))):
                    return 'F', 0, 0, SOLUTION_FAIL.format(case[0], case[1], ''.join(output))

                # checker program only print '0' or '1'
                elif self.problem_type == 'C':
                    if int(output[0]) == 0:
                        return 'F', 0, 0, CHECK_FAIL.format(case[0], ''.join(output))
                    elif int(output[0]) != 1:
                        return 'P', 0, 0, PROBLEM_ERROR.format('CHECKER 출력 문제')
            else:
                return 'E', 0, 0, SEVER_ERROR

        return 'S', self.total_time/testcase_cnt, self.total_memory/testcase_cnt, ''

    def make_command(self, path, run_command):
        command = run_command.split(',')
        command = [path if path else command[0]] + command
        return command

    def check_output(self, output, answer, is_follow=False):
        if is_follow:
            out = re.sub(r'[\n\r\t ]+', '', output)
            ans = re.sub(r'[\n\r\t ]+', '', answer)
            return out == ans

        if len(output) != len(answer):
            return False

        for idx in range(len(output)):
            out = output[idx].rstrip()
            ans = answer[idx].rstrip()

            if out != ans:
                return False

        return True