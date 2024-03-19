import re
import time

import requests


def post_task(url_status, list, param):
    url_test = "http://223.223.187.26:63333/api/v1/task/test"  # POST请求的URL地址
    url_add = "http://223.223.187.26:63333/api/v1/task/add"  # POST请求的URL地址
    task_id = ""  # task_id的值
    count = 0
    if param == 1:
        post_data = {
            "task_param": {
                "source_data": list,
                "source": "naz.api",
                "country": "",
                "province": "",
                "line_old_mapping": {
                    "url": 0,
                    "account": 1,
                    "email": 3,
                    "password": 2
                },
                "mapping_key": {
                    "account": "account",
                    "email": "email",
                    "msg.pwd": "password",
                    "original_other": "url"
                },
                "key": ["original_other", "account"]
            }
        }
    else:
        post_data = {
            "task_param": {
                "source_data": list,
                "source": "naz.api",
                "country": "",
                "province": "",
                "line_old_mapping": {
                    "url": 0,
                    "account": 1,
                    "password": 2
                },
                "mapping_key": {
                    "account": "account",
                    "msg.pwd": "password",
                    "original_other": "url"
                },
                "key": ["original_other", "account"]
            }
        }
    headers = {
        "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI0OTU5MzU2NTYsImlhdCI6MTYzMTkzNTY1NiwibmJmIjoxNjMxOTM1NjU2LCJpZGVudGl0eSI6IjEifQ.utYwffiPOuLI8gh-_YF4_8wdF5kf22QuCnUORQf81NM"}  # 设置请求头部信息（根据接口要求进行配置）

    if url_status == 0:
        url = url_test
        response = requests.post(url, json=post_data, headers=headers)  # 发送POST请求并获取响应结果
    elif url_status == 1:
        url = url_add
        response = requests.post(url, json=post_data, headers=headers)  # 发送POST请求并获取响应结果
        match = re.search(r'"task_id":"(.*?)"', response.text)
        if match:
            # 提取匹配到的值
            task_id = match.group(1)
        with open('log1.log', 'a') as log:
            while True:
                status = 5
                response_1 = get_status(task_id)
                print(response_1.text)
                log.write(response_1.text)
                match_1 = re.search(r'"status"\s*:\s*"(.*?)"', response_1.text)
                if match_1:
                    # 提取匹配到的值
                    status = match_1.group(1)
                    print("匹配到状态码了")
                    print(status)
                if status == 'finished':
                    break
                count += 1
                if count == 10:
                    stop_task(task_id)
                    log.write(f"停掉了{task_id}任务")
                    break

                time.sleep(3)
    else:
        print("状态码有问题")
        return

    return (response.text)  # 输出响应内容


### 查询状态
def get_status(task_id):
    url = f"http://223.223.187.26:63333/api/v1/task/status/{task_id}"
    headers = {
        "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI0OTU5MzU2NTYsImlhdCI6MTYzMTkzNTY1NiwibmJmIjoxNjMxOTM1NjU2LCJpZGVudGl0eSI6IjEifQ.utYwffiPOuLI8gh-_YF4_8wdF5kf22QuCnUORQf81NM"
    }  # 设置请求头部信息（根据接口要求进行配置）
    response = requests.get(url, headers=headers)
    return response


def stop_task(task_id):
    url = "http://223.223.187.26:63333/api/v1/task/stop"
    headers = {
        "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI0OTU5MzU2NTYsImlhdCI6MTYzMTkzNTY1NiwibmJmIjoxNjMxOTM1NjU2LCJpZGVudGl0eSI6IjEifQ.utYwffiPOuLI8gh-_YF4_8wdF5kf22QuCnUORQf81NM"
    }
    data = {"task_id": task_id}
    response = requests.post(url, headers=headers, json=data)
    return response
