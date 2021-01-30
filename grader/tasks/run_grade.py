import json
import requests

from grade_core.compile import Compile
from grade_core.grade import Grade
from grade_core.utils import safety_file_open
from grade_core.message import PROBLEM_ERROR, SEVER_ERROR


BASE_URL = ''
PLATFORM_URL =  ''


def send_result(result, avg_time, avg_mem, message, log_id, submit_id):
        res = requests.put('{}/api/v1/submit/{}/'.format(BASE_URL, log_id),
                           data={
                               'result': result,
                               'message': message,
                               'other_info': '{},{}'.format(int(avg_time), int(avg_mem)),
                           })
        if res.status_code != 200:
            print(res.text)
            print(res.content)

        res = requests.put('{}/design/problem/update-submit/{}'.format(PLATFORM_URL, submit_id),
                           data={
                               'result': result,
                               'message': message,
                               'avg_time': int(avg_time),
                               'avg_memory': int(avg_mem),
                           })
        if res.status_code != 200:
            print(res.text)
            print(res.content)


def grade(grading_info):
    try:
        # compile
        print('### Start Compile ###')
        if grading_info['problem_type'] != 'F':
            code_compile = Compile()
            if not code_compile(grading_info['extension'], grading_info['compile_path'],
                                grading_info['compile_command'], grading_info['submit_code'],
                                grading_info['file_name']):
                _, msg = safety_file_open('error.err')
                send_result('C', 0, 0, ''.join(msg), grading_info['log_id'], grading_info['submit_id'])
                return

            if grading_info['problem_type'] == 'C':
                if not code_compile(grading_info['checker__language__extension'],
                                    grading_info['checker__language__compile_path'],
                                    grading_info['checker__language__compile_command'].replace('main', 'checker'),
                                    grading_info['checker__language__submit_code']):
                    send_result('P', 0, 0, PROBLEM_ERROR.format('CHECKER 컴파일 에러'),
                                grading_info['log_id'], grading_info['submit_id'])
                    return
        print('### End Compile ###')

        # grade
        print('### Start Grading ###')
        grade_code = Grade(grading_info['time'],
                           grading_info['memory'],
                           grading_info['problem_type'])
        result, avg_time, avg_mem, message = grade_code(grading_info)
        print('### End Grading ###')
        send_result(result, avg_time, avg_mem, message, grading_info['log_id'], grading_info['submit_id'])
    except Exception as e:
        send_result('E', 0, 0, SEVER_ERROR, grading_info['log_id'], grading_info['submit_id'])


if __name__ == '__main__':
    # with open('/home/algorithm/grade/backend/grader/tasks/json_data_volume/matchdata.json') as json_file:
    with open('/grading_info.json') as json_file:
        grading_info = json.load(json_file)
    grade(grading_info)