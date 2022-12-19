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
    _password = _user
    isReached = ''
    
    # если хост достигнут
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
            stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && svn info --show-item url')  # папка ~/bw/ 
            branch = stdout.readlines()[0].rstrip()

            stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && svn info --show-item revision')  # папка ~/bw/ 
            revision = stdout.readlines()[0].rstrip()
            ssh.close()

        except:
            stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && git rev-parse --abbrev-ref HEAD')  # папка ~/bw/ 
            branch = stdout.readlines()[0].rstrip()

            stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && git rev-list --count HEAD')  # папка ~/bw/ 
            revision = stdout.readlines()[0].rstrip()
            ssh.close()

        file_json['hosts'][f'{_cluster}']['branch'] = branch
        file_json['hosts'][f'{_cluster}']['revision'] = revision
        file_json['hosts'][f'{_cluster}']['isReach'] = isReached

    #если и Git и SVN отсутствуют
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

  
########### Запись в файл с оставлением бекапа ###########
if validateJSON(json.dumps(file_json)) == True:
    os.rename('JSON.json', f'JSON.json.back{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}')
    with open('JSON.json', 'w') as outfile:
        json.dump(file_json, outfile, indent=2)
        outfile.close()
    logging.info('file update successfully')
else:
    logging.info('invalid JSON')

logging.info('Complete!')
