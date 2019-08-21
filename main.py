# -*- coding:utf-8 -*-
import json
import requests
from config import *

__author__ = 'mxj'
__date__ = '2019/8/20 15:36'




class ApiTest(object):

    def __init__(self,url=None,port=None,username=None,password=None):

        self.url = url or default_url
        self.port = port or default_port
        self.username = username or default_username
        self.password = password or default_password
        self.prefix = "http://%s:%s" % (self.url, self.port)
        self.login_url = "%s/login" % self.prefix
        self.logout_url = "%s/logout" % self.prefix
        self.login()

    def login(self):
        """使用session登录"""
        with requests.Session() as session:
            # provide authentication data to session, will be sent automatically
            session.auth = (self.username, self.password)
            # Use the first request, which uses basic authentication, to set the language using the cookie
            resp = session.post(self.login_url)
            if resp.status_code == 200:
                # Accessing resp.json() will automatically decode the response payload
                session.headers['X-Csrf-Token'] = resp.cookies._cookies[self.url]['/']['CSRFToken'].value
                session.headers['Content-Type'] = 'application/json'
                self.session = session
                print('-------------登陆成功-------------')

            else:
                raise Exception("-------------登陆失败！状态码：%s-------------" % resp.status_code)

    def logout(self):
        """退出登录"""
        self.session.get(self.logout_url)
        print("-------------您已退出登录-------------")


    def get_loop(self):
        """循环get查询"""
        print("-------------开始get查询-------------")
        urls = {}
        while True:
            try:
                print("-------------输入url或已输入过的url对应的key-------------")
                print(urls)
                url = input("url:")
                if url=='break':
                    break
                if url.isdigit():
                    url = urls.get(url,'')
                if url.strip():
                    urls[str(len(urls) + 1)] = url
                    self.get(url)
                else:
                    print("输入url有误")
            except Exception as e:
                print(str(e))

    def post_loop(self):
        print("-------------开始post查询-------------")
        urls = {}
        while True:
            try:
                print("-------------输入url或已输入过的url对应的key-------------")
                print(urls)
                url = input("输入url:")
                if url=='break':
                    break
                json = input("输入json数据:")
                if json=='break':
                    break
                if url.isdigit():
                    url = urls.get(url,'')
                if url.strip():
                    urls[str(len(urls)+1)] = url
                    self.post(url,json)
                else:
                    print("输入有误")
            except Exception as e:
                print(str(e))

    def get(self,url):
        """get查询"""
        url = self.prefix + url
        res = self.session.get(url)
        print("---------------%s 返回值--------------"%url)
        print(json.dumps(res.json(), indent=4))
        print("---------------------------------------分割线------------------------------------------------------")

    def post(self,url,json):
        """post查询"""
        url = self.prefix + url
        res = self.session.post(url,json=json)
        print("---------------%s 返回值--------------"%url)
        print(res.json())
        print("---------------------------------------分割线------------------------------------------------------")

if __name__ == '__main__':
    get = ApiTest()
    # get.get_loop()
    get.post_loop()
