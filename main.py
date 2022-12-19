import paramiko
import json
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

########### Логирование ###########
logging.basicConfig(handlers=[RotatingFileHandler("logs/test.log", maxBytes=500000, backupCount=10)],
                    level=logging.INFO, format='%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')
logging.info('Starting!')

########### Открытие файла ###########
with open('JSON.json') as f:
    file_json = json.load(f)

cluster = file_json['hosts']
for item in cluster:
    _cluster = item
    _host = cluster[item]['host']
    _user = cluster[item]['user']
    _password = '5549'  # _user
    isReached = ''

    # if 'win' in platform:
    # print('windows')
    # winuser = os.getlogin()
    # if os.path.file(f'C:\Users\{winuser}/.ssh/id_rsa'):
    #    try:
    #        ssh = paramiko.SSHClient()
    #        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #        ssh.load_system_host_keys()
    #        privkey = paramiko.RSAKey.from_private_key_file(f'C:\Users\{winuser}/.ssh/id_rsa')
    #        ssh.connect(
    #            hostname=_host,
    #            username=_user,
    #            pkey=privkey,
    #        )
    #    except:
    #        logging.info("except")

    # else:
    # print('linux')
    # if os.path.file('~/.ssh/id_rsa'):
    #    try:
    #        ssh = paramiko.SSHClient()
    #        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #        ssh.load_system_host_keys()
    #        privkey = paramiko.RSAKey.from_private_key_file('~/.ssh/id_rsa')
    #        ssh.connect(
    #            hostname=_host,
    #            username=_user,
    #            pkey=privkey,
    #        )
    #    except:
    #        logging.info("except")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=_host,
            username=_user,
            password=_password
        )
        isReached = 'Yes'
        logging.info('Connected to the host: ' + _host + ' and the user: ' + _user)

    # если хост не достигнут
    except:
        logging.warning('Can not connect to the host: ' + _host + ' and the user: ' + _user)
        isReached = 'No'
        branch = 'None'
        revision = 'None'

    ########### Проверка веток и ревизий ###########
    try:
        try:
            stdin, stdout, stderr = ssh.exec_command('cd ~/git/test-repo && svn info --show-item url')  # папка
            branch = stdout.readlines()[0].rstrip()

            stdin, stdout, stderr = ssh.exec_command('cd ~/git/test-repo && svn info --show-item revision')  # папка
            revision = stdout.readlines()[0].rstrip()
            ssh.close()

        except:
            stdin, stdout, stderr = ssh.exec_command('cd ~/git/test-repo && git rev-parse --abbrev-ref HEAD')  # папка
            branch = stdout.readlines()[0].rstrip()

            stdin, stdout, stderr = ssh.exec_command('cd ~/git/test-repo && git rev-list --count HEAD')  # папка
            revision = stdout.readlines()[0].rstrip()
            ssh.close()

        file_json['hosts'][f'{_cluster}']['branch'] = branch
        file_json['hosts'][f'{_cluster}']['revision'] = revision
        file_json['hosts'][f'{_cluster}']['isReach'] = isReached

    #если Git и SVN отсутствуют
    except:
        branch = 'None'
        revision = 'None'
        file_json['hosts'][f'{_cluster}']['branch'] = branch
        file_json['hosts'][f'{_cluster}']['revision'] = revision
        file_json['hosts'][f'{_cluster}']['isReach'] = isReached

    logging.info('branch: ' + branch + ' | revision: ' + revision)


########### Валидация JSON файла ###########
def validateJSON(jsonData):  # проверка json на валидность
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

'''
try:
    json.dumps(json.loads(file_json))
    os.rename('JSON.json', f'JSON.json.back{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}')
    with open('JSON.json', 'w') as outfile:
        json.dump(file_json, outfile)
        outfile.close()
except:
    print('error:')
'''

########### Запись в файл с оставлением бекапа ###########
if validateJSON(json.dumps(file_json)) == True:
    print('valid')
    os.rename('JSON.json', f'JSON.json.back{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}')
    with open('JSON.json', 'w') as outfile:
        json.dump(file_json, outfile, indent=2)
        outfile.close()
    logging.info('file update successfully')
else:
    print('invalid JSON ')

# print(type(file_json))

logging.info('Complete!')
