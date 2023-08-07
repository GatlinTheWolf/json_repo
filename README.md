# json_repo
Python paramiko json  

There is a list of users and hosts, followed by "JSON"
"""
{
    "hosts": {
        "EU-CLUSTER": {
            "title": "Eu cluster discription",
            "host": "eu1-vm-host",
            "user": "euuser"
        },
        "NA-CLUSTER": {
            "title": "Na cluster description",
            "host": "na1-vm-host",
            "user": "nauser"
        }
    }
}
"""
1.Authorization to ssh host can occur either by ssh key or by password, which equals user, that is, for user1 user, user1 password, if user has no key.
2.Each user in the directory ~/bw/ may have a working copy of git or subversion. You must write a script that
3.Runs on all JSON users
4.Collects information about the working copy, namely 
    A) For git, it learns which branch the working copy is following and which revision it is on. 
    B) for subversion knows which branch is in the working copy and which revision.
5.Adds to the original JSON collected information from points 4.A, 4.B.

Python paramiko json
Есть список пользователей и хостов, далее "JSON"
"""
{
    "hosts": {
        "EU-CLUSTER": {
            "title": "Eu cluster discription",
            "host": "eu1-vm-host",
            "user": "euuser"
        },
        "NA-CLUSTER": {
            "title": "Na cluster description",
            "host": "na1-vm-host",
            "user": "nauser"
        }
    }
}
"""
1) Авторизация на ssh host может происходить либо по ssh ключу, либо по password, который равен user,
то есть для пользователя user1, пароль user1, если у пользователя нет ключа.
2) У каждого пользователя user в директории ~/bw/ может быть рабочая копия git или subversion.
Необходимо написать скрипт, который
3) Проходит по всем пользователям из JSON
4) Собирает информацию о рабочей копии, а именно
    А) Для git узнаёт за какой веткой следит данная рабочая копия и на какой ревизии она находится.
    Б) для subversion узнаёт какая ветка находится в рабочей копии и на какой ревизии.
6) Добавляет в изначальный JSON собранную информацию из пунктов 4.А, 4.Б.
