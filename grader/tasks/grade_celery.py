import os
import time
import json
import docker
import random
import logging
import multiprocessing
from billiard import current_process

from backend.celery import app
from .. import models


MAX_SIZE = int((multiprocessing.cpu_count() - 1) * 1.8)
logger = logging.getLogger(__name__)


@app.task(name='grade_code')
def grade_code(log_id, problem_id, submit_id, submitlog_code, file_name, language_id):
    mode = 'develop'
    docker_img = 'core'
    volume_path = os.path.join(os.getcwd(), 'grader', 'tasks', 'json_data_volume')

    try:
        print('### Data Setting ###')
        grading_info = models.Problem.objects.prefetch_related(
            'checker__language',
        ).filter(
            id=problem_id,
        ).values(
            'problem_type',
            'time', 'memory',
            'case_count',
            'checker__code',
            'checker__language__extension',
            'checker__language__compile_path',
            'checker__language__compile_command',
            'checker__language__run_path',
            'checker__language__run_command',
        )[0]

        command = models.Language.objects.filter(
            id=language_id
        ).values(
            'extension', 'compile_path', 'compile_command',
            'run_path', 'run_command'
        )[0]
        for key in command:
            grading_info[key] = command[key]

        testcase = list(
            models.TestCase.objects.filter(
                problem_id=problem_id,
            ).values_list(
                'input', 'output'
            )
        )
        grading_info['testcase'] = testcase
        print(submitlog_code)
        grading_info['submit_code'] = submitlog_code
        grading_info['file_name'] = file_name
        grading_info['submit_id'] = submit_id
        grading_info['log_id'] = log_id
        print('### End Setting ###')

        ####### TEST CODE #######
        # file_name = 'matchdata.json'
        # data_file_path = os.path.join(volume_path, file_name)
        # with open(data_file_path, 'w') as fp:
        #     json.dump(grading_info, fp)
        # os.system('python3 /home/algorithm/grade/backend/grader/tasks/run_grade.py')
        # return
        #########################

        ###############################
        worker_num = current_process().index
        docker_name = '{}-'.format(worker_num)
        while True:
            run_cnt = get_container_list(worker_num)
            if run_cnt < MAX_SIZE:
                docker_name += '{}{}{}{}{}'.format(random.choice(['A', 'B', 'C', 'D']),
                                                   log_id, problem_id, submit_id, language_id)
                break
            time.sleep(0.3)
        print('### Run Grading in Container {} ###'.format(docker_name))

        # docker setting
        client = docker.from_env()

        # create data file
        try:
            file_name = 'matchdata_{}_{}.json'.format(grading_info['submit_id'], random.randint(100, 10000))
            data_file_path = os.path.join(volume_path, file_name)
            with open(data_file_path, 'w') as fp:
                json.dump(grading_info, fp)

        except Exception as e:
            print(f'Fail Create matchdata.json file: {e}')

        # run container
        volumes = {data_file_path: {'bind': '/grading_info.json', 'mode': 'rw'}}
        try:
            if mode == 'develop':
                client.containers.run(image=docker_img, command='python3 run_grade.py', volumes=volumes,
                                      mem_limit='1g', detach=True,
                                      name=docker_name, auto_remove=True, privileged=True, network_mode='host')
            else:
                client.containers.run(image=docker_img, command='python3 run_grade.py', volumes=volumes,
                                      mem_limit='1g', detach=True,
                                      name=docker_name, auto_remove=True, privileged=True)
        except Exception as e:
            print(f'Fail run docker container: {e}')

    except Exception as e: #models.Problem.DoesNotExist:
        print(e)
        return

def get_container_list(worker_num):
    cnt = 0
    running_containers = docker.APIClient().containers()
    for container in running_containers:
        w_num = int(container['Names'][0][1:].split('-')[0])
        if w_num == worker_num:
            cnt += 1
    return cnt

def check_task_order():
    n = 0
    i = app.control.inspect().active()
    for key in i:
        n += len(i[key])
    return n
