import os
import time
import json
import docker
import random
import logging
import multiprocessing

from backend.celery import app
from .. import models


CONTAINER_LIST = [i for i in range(1, multiprocessing.cpu_count())]
logger = logging.getLogger(__name__)


@app.task(name='grade_code')
def grade_code(log_id, problem_id, submit_id, code, language_id):
    mode = 'develop'
    docker_img = 'core'
    volume_path = os.path.join(os.getcwd(), 'grader', 'tasks', 'json_data_volume')

    try:
        print('### Data Setting ###')
        grading_info = models.Problem.objects.filter(
            id=problem_id,
        ).values(
            'problem_type',
            'time', 'memory',
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

        grading_info['submit_code'] = code
        grading_info['submit_id'] = submit_id
        grading_info['log_id'] = log_id
        print('### End Setting ###')

        ####### TEST CODE #######
        # file_name = 'matchdata.json'
        # data_file_path = os.path.join(volume_path, file_name)
        # with open(data_file_path, 'w') as fp:
        #     json.dump(grading_info, fp)
        # os.system('python3 /home/algorithm/grade/backend/grader/tasks/run_grade.py')
        #########################

        ###############################
        docker_name = '00'
        while True:
            run_containers = get_container_list()
            usable_containers = set(CONTAINER_LIST) - set(run_containers)
            if usable_containers:
                docker_name += str(usable_containers.pop())
                break
            time.sleep(1)
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
                                      cpuset_cpus=docker_name, mem_limit='1g', detach=True,
                                      name=docker_name, auto_remove=True, privileged=True, network_mode='host')
            else:
                client.containers.run(image=docker_img, command='python3 run_grade.py', volumes=volumes,
                                      cpuset_cpus=docker_name, mem_limit='1g', detach=True,
                                      name=docker_name, auto_remove=True, privileged=True)
        except Exception as e:
            print(f'Fail run docker container: {e}')

    except Exception as e: #models.Problem.DoesNotExist:
        print(e)
        return

def get_container_list():
    c_list = []
    running_containers = docker.APIClient().containers()
    for container in running_containers:
        c_list.append(int(container['Names'][0][1:]))
    return c_list

def check_task_order():
    n = 0
    i = app.control.inspect().active()
    for key in i:
        n += len(i[key])
    return n
