import logging
import os.path
import time
from threading import Thread

import requests
from bs4 import BeautifulSoup
import execjs

from logging import Logger


# noinspection HttpUrlsUsage
class Auth(Thread):
    def __init__(self, userid, password, retry):
        super().__init__()
        self.userid = userid
        self.password = password
        self.__retry = retry

        self.lib_url = "http://seat.lib.sdu.edu.cn/home/web/f_second"
        self.auth_url = "http://seat.lib.sdu.edu.cn/cas/index.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36",
        }

        self.lt, self.execution, self._eventId = None, None, None
        self.rsa = None

        self.session = requests.session()
        self.session.headers.update(self.headers)

        self.__already_login = False
        self.__logger: Logger = logging.getLogger()

    def __gather_trivial(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            self.lt = soup.select_one("#lt").get("value")
            self.execution = soup.select_one("[name=execution]").get("value")
            self._eventId = soup.select_one("[name=_eventId]").get("value")
        except TypeError as e:
            self.__logger.error(e)

        if self.lt and self.execution and self._eventId is None:
            raise AuthException("未获取到用户登陆所需的所有信息")

    def __get_rsa(self):
        with open(os.path.join(os.path.dirname(__file__), "../util/des.js"), encoding="utf-8") as f:
            js = f.read()
            f.close()
        self.rsa = execjs.compile(js).call('strEnc', self.userid + self.password + self.lt, "1", "2", "3")
        if self.rsa is None:
            raise AuthException("未获取DES加密的用户信息")

    def __phase1(self, url):
        data = {
            "ul": str(len(self.userid)),
            "pl": str(len(self.password)),
            "lt": self.lt,
            "execution": self.execution,
            "_eventId": self._eventId,
            "rsa": self.rsa
        }
        res = self.session.post(url, data=data, allow_redirects=False)
        self.__logger.info('Status code for phase-1-response is {}'.format(res.status_code))
        if res.status_code != 302:
            raise AuthException('阶段1：响应状态码为{}, 认证失败'.format(res.status_code))
        url = res.headers.get("Location").replace(' ', '')
        if url.startswith("/cas/login?service="):
            url = url.replace("/cas/login?service=", "")

        return url

    def __phase2(self, url):
        res = self.session.get(url, allow_redirects=True)
        self.__logger.info('Status code for phase-2-response is {}'.format(res.status_code))
        if res.status_code != 200:
            raise AuthException('阶段2：响应状态码为{}, 认证失败'.format(res.status_code))
        return res.status_code

    def login(self):

        # GET 图书馆认证界面 302 -> 统一身份认证界面
        res = self.session.get(self.auth_url, allow_redirects=True)
        # 从统一身份认证界面获取必要信息
        self.__gather_trivial(res.text)
        # 加密脚本
        self.__get_rsa()
        # POST 统一身份认证 发送认证信息
        url = self.__phase1(res.url)

        # 切换HEADER绕过检查再进行重定向
        self.session.headers.update({
            'Host': 'seat.lib.sdu.edu.cn'
        })
        self.__phase2(url)

        # 如果最终获取到这几个必要cookie则说明登陆成功
        if self.session.cookies['userid'] and self.session.cookies['user_name'] and\
                self.session.cookies['user_name'] and self.session.cookies['access_token'] is None:
            raise AuthException("登陆失败")
        else:
            self.__already_login = True
            self.__logger.info('Login successfully!')

    def success(self) -> bool:
        return self.__already_login

    def reset(self):
        self.session.close()
        self.session = requests.session()
        self.session.headers.update(self.headers)

        self.__already_login = False

    def run(self) -> None:
        # Retry until login successfully.
        count = 0
        while count < self.__retry and not self.success():
            count += 1
            try:
                self.login()
            except EnvironmentError as env:
                logging.error('系统环境导致认证进程出现异常{}，请检查'.format(env))
                time.sleep(30)
            except AuthException as e:
                logging.error(e)
                time.sleep(30)
        return


class AuthException(Exception):
    pass
