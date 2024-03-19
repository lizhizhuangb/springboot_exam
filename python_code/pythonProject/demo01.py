import json
from time import sleep
import utils.post

file = r'D:\download_1\00 (2).txt'
url_status = 1
with open(file, 'r', encoding='utf-8', errors='ignore') as f:
    list_1 = []  # 网址~邮箱~密码
    list_2 = []  # 网址~用户名~密码

    for line in f:
        data = line.split(":")
        data_1 = ['', '', '', '']
        if not data[0].startswith(('http', 'https')):
            continue
        if len(data) != 4:
            continue
        data[3] = data[3].replace('\n', '')
        data_1[0] = data[0] + data[1]
        data_1[1] = data[2]
        data_1[2] = data[3]
        data_1[3] = data[2]
        if '@' in data[2]:

            list_1.append(data_1)
            # sleep(1)
            if len(list_1) == 50000:
                print(utils.post.post_task(url_status, list_1, 1))
                list_1 = []


        else:
            list_2.append(data_1)
            if len(list_2) == 50000:
                print(utils.post.post_task(url_status, list_2, 2))
                list_2 = []

    if list_1:
        print(utils.post.post_task(url_status, list_1, 1))
    if list_2:
        print(utils.post.post_task(url_status, list_2, 2))


