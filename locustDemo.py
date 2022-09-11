import json
import time
from locust import HttpUser, task, between, events, TaskSet
import urllib3

# 禁用安全请求警告
urllib3.disable_warnings()


def res_assert(req, string):
    try:
        responses = json.loads(req.text)
        # print(responses)
        # 状态码断言
        if req.status_code == 200:
            if responses['message'] == '成功!':
                print(f"{string}成功")
            else:
                print(f"{string}失败" + "code:{},message:{}".format(responses['code'], responses['message']))
        else:
            print(f"{string}失败" + "status_code:%s，message:%s" % (req.status_code) % (responses['message']))
    except Exception as E:
        print(E)


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')


@events.test_stop.add_listener
def on_test_stop(**kwargs):

    print('===测试结束了提示===')


class Case(TaskSet):
    def on_start(self):
        print('每次实例化前都会执行')

    @task(30)  # taks 装饰器 可控制任务执行权重比
    def getTime(self):
        header = {"accept": "application/json"}
        req = self.client.get(url="/getTime", headers=header, verify=False)
        res_assert(req, 'getTime')

    @task(20)
    def getSentences(self):
        header = {"accept": "application/json"}
        req = self.client.get(url="/sentences", headers=header, verify=False)
        res_assert(req, 'getSentences')

    @task(5)
    def getLogin(self):
        header = {"accept": "application/json", "Content-Type": "application/json",
                  "content-type": "application/x-www-form-urlencoded"}
        bodys = {"account": "m59559@126.com", "password": "m59559"}
        req = self.client.post(url="/login", headers=header, data=bodys, verify=False)
        res_assert(req, 'getLogin')

    def on_stop(self):
        print('每次销毁实例时都会执行')


class TestTask(HttpUser):
    tasks = [Case]
    wait_time = between(1, 5)
    # min_wait = 2000  #每个用户执行两个任务间隔时间的上下限（毫秒）
    # max_wait = 5000  #具体数值在上下限中随机取值，默认间隔时间固定为1秒；


if __name__ == "__main__":
    import os
    os.system("locust -f locustDemo.py --host=https://api.apiopen.top/api")
