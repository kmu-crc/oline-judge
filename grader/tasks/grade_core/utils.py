def safety_file_write(path, data):
    try:
        with open(path, 'w') as fp:
            fp.write(data)
    except Exception as e:
        print('file write error')
        print(e)
        return False
    return True


def safety_file_open(path):
    try:
        with open(path, 'r') as fp:
            data = fp.readlines()
    except Exception as e:
        print('file open error')
        print(e)
        return False, []
    return True, data
