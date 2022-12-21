import paramiko
import json
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler
import sys


########### Логирование ###########
logging.basicConfig(handlers=[RotatingFileHandler("logs/logfile.log", maxBytes=500000, backupCount=10)],
                    level=logging.INFO, format='%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')
logging.info('Starting!')


def main():
    try:  # Открытие файла JSON.json
        with open('JSON.json') as f:
            file_json = json.load(f)
    except:
        logging.warning('Can not read JSON')
        print('Can not read JSON')
        sys.exit(1)

    cluster = file_json['hosts']
    for item in cluster:
        _cluster = item
        _host = cluster[item]['host']
        _user = cluster[item]['user']
        _password = _user
        isReached = ''

    ########### Подключение к хосту ###########
        try:  # если удалось подключиться
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=_host,
                username=_user,
                password=_password
            )
            isReached = 'Yes'
            logging.info(f'Connected to host: {_host} and user: {_user}')
            print(f'Connected to host: {_host} and user: {_user}')

        except:  # если не удалось подключиться
            isReached = 'No'
            branch = 'None'
            revision = 'None'
            file_json['hosts'][f'{_cluster}']['branch'] = branch
            file_json['hosts'][f'{_cluster}']['revision'] = revision
            file_json['hosts'][f'{_cluster}']['isReach'] = isReached
            logging.warning(f'Can not connect to host: {_host} and user: {_user}')
            print(f'Stop looking for a Git and SVN in host {_host}')
            continue

        ########### Проверка веток и ревизий ###########
        try:
            try:  # eсли SVN
                stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && svn info --show-item url')
                branch = stdout.readlines()[0].rstrip()

                stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && svn info --show-item revision')
                revision = stdout.readlines()[0].rstrip()
                ssh.close()

            except:  # eсли GIT
                stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && git rev-parse --abbrev-ref HEAD')
                branch = stdout.readlines()[0].rstrip()

                stdin, stdout, stderr = ssh.exec_command('cd ~/bw/ && git rev-list --count HEAD')
                revision = stdout.readlines()[0].rstrip()
                ssh.close()

            file_json['hosts'][f'{_cluster}']['branch'] = branch
            file_json['hosts'][f'{_cluster}']['revision'] = revision
            file_json['hosts'][f'{_cluster}']['isReach'] = isReached

        except:  # если Git и SVN отсутствуют
            branch = 'None'
            revision = 'None'
            file_json['hosts'][f'{_cluster}']['branch'] = branch
            file_json['hosts'][f'{_cluster}']['revision'] = revision
            file_json['hosts'][f'{_cluster}']['isReach'] = isReached

        logging.info('branch: ' + branch + ' | revision: ' + revision)

    ########### Валидация и запись JSON файла ###########
    try:
        os.rename('JSON.json', f'JSON.json.back{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}')  # бекап JSON файла
        with open('JSON.json', 'w') as outfile:
            json.dump(file_json, outfile, indent=2)
            outfile.close()
            print('Complete!')
            logging.info('Complete!')
    except:
        print('Invalid JSON')
        logging.warning('Validation or writing error')

if __name__ == "__main__":
    main()
