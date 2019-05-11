# -*- coding: utf-8 -*-

"""
Scripts for login school wifi 江苏科技大学 张家港校区/苏州理工学院
"""
import requests
import sys
import json
import logging
import os
import base64


# TODO(smokecatyo@gmail.com) Path problem
def check_ping(url):
    """ping"""
    logging.info('ping {}'.format(url))
    result_code = os.system('ping -n 1 {} > nul'.format(url))
    print('finish ping! result code: {}'.format(result_code))
    logging.info('the result code of ping: {}'.format(result_code))

    return result_code


class Login(object):
    """Login object"""

    def __init__(self):
        """Constructor"""
        self._url_get = 'http://10.3.130.12'

        self._url_post = 'http://10.3.130.12/index.php/index/login'

        # define the headers for get requests
        self._headers_get = None

        # define the headers for post requests
        self._headers_post = None

        # define the data for post requests
        self._data_post = None

        # define the cookies for post requests
        self._cookies_post = {}

        # define the config file name
        self._data_post_file = sys.path[0]+'/conf/data_post.json'
        self._conf_file = sys.path[0] + '/conf/configure.json'

        # define the content-length message
        self._content_len_msg = None

    def load_conf(self):
        """"""
        with open(self._data_post_file, encoding='utf-8') as f:
            self._data_post = json.load(f)
        # 密码进行base64加密
        self._data_post['password'] = base64.b64encode(bytes(self._data_post['password'], encoding='utf-8'))
        logging.info('post data: username={}, domain={}'.format(self._data_post['username'], self._data_post['domain']))

        with open(self._conf_file, encoding='utf-8') as f:
            conf = json.load(f)
            self._content_len_msg = conf['content-length']
            self._headers_get = conf['get-headers']
            self._headers_post = conf['post-headers']

        print(self )

    def req_get(self):
        """
        Send the requests with GET method.
        Set the self._cookies_post from the response.
        """
        # check the JUST
        print('check the connection to JUST ...')
        result_code = check_ping(self._url_get.split('://')[1])
        if result_code != 0:
            print('检查是否成功连接JUST校园网')
            # TODO(smokecatyo@gmail.com) Package exit(0) into function and add logging.info()
            sys.exit(0)

        print('run the first request: get({}) ...'.format(self._url_get))
        try:
            response = requests.get(self._url_get, headers=self._headers_get)
        except requests.ConnectionError:
            logging.warning('find request.ConnectionError!, check the connection to JUST')
            print('请检查是否成功连接上JUST校园网')
            sys.exit(0)
        except requests.RequestException:
            logging.warning('find requests.RequestException!')
            print('出现错误')
            sys.exit(0)
        else:
            logging.info('get successfully!')
            print('successfully!')
            print('code: {}'.format(response.status_code))

        # Get the Cookies from the response
        # 注意:
        # 抓包发现有在返回的response的headers中有两个'Set-Cookie',类似：
        #     Set-Cookie: think_language=zh-CN; expires=Sat, 01-Jun-2000 12:00:00 GMT; path=/\r\n
        #     Set-Cookie: PHPSESSID=fkzxcyu19sdfiou3crcnzklcj3; path=/\r\n
        # 通过request.Response.headers['Set-Cookie'}获得的是合并后的结果，中间用','分隔,例如:
        #     'think_language=zh-CN; expires=Sat, 01-Jun-2000 12:00:00 GMT; path=/,
        #     PHPSESSID=fkzxcyu19sdfiou3crcnzklcj3; path=/'
        # 需要处理后才能使用，并且后续发送post请求时只不需要path字段
        cookies = response.headers['Set-Cookie']
        logging.info('get original cookies: {}'.format(cookies))

        # print('get the cookies from get_response: {}'.format(cookies))
        cookies = cookies.replace('path=/,', '').replace('path=/', '')

        # print('after handling the original cookies: {}'.format(cookies))
        for line in cookies.split(';'):
            if not line.strip():
                continue
            k, v = line.strip().split('=', 1)
            self._cookies_post[k] = v

        # print('the cookies set to post request: {}'.format(self._cookies_post))

    def req_post(self):
        """
        Send the request with POST method.
        Finish the authenticate
        """
        print('run the second request: post({}) ...'.format(self._url_post))
        try:
            response = requests.post(self._url_post, data=self._data_post,
                                     cookies=self._cookies_post, headers=self._headers_post)
        except requests.RequestException:
            logging.warning('find requests.RequestException!')
            print('出现错误')
            sys.exit(0)
        else:
            logging.info('post successfully!')
            content_length = response.headers['Content-Length']

            print('successfully!')
            print('code: {}'.format(response.status_code))
            print('content-length: {}'.format(content_length))

        # 无法通过status_code判断认证结果，返回的都是200，凭借Content-Length可以大致判断，但不排除例外情况
        # Content-Length
        #       49:密码错误
        #       241:正确
        #       206:账号错误
        #       64:已经登录
        #       125:domain错误
        logging.info('Content-Length={}: {}'.format(content_length, self._content_len_msg[content_length]))
        if content_length in self._content_len_msg:
            print('it\'s possible meaning: {}'.format(self._content_len_msg[content_length]))
        else:
            print('unknown num')

        # check the connection to the Internet
        logging.info('after post: check Internet')
        print('check the connection to the Internet ...')
        result_code = check_ping('mirrors.aliyun.com')
        if result_code != 0:
            print('无法连接到互联网，认证校园网失败, 请手动检查连接或查询错误')
            sys.exit(0)
        else:
            print('成功连接到互联网，认证成功！')


def main():
    """Login the wifi"""
    # set log config
    logging.basicConfig(filename=sys.path[0]+'/log/login.log', level=logging.DEBUG,
                        format='%(asctime)s %(filename)s %(levelname)s: %(message)s',
                        datefmt='%Y/%m/%d %a %H:%M:%S')
    logging.info('run the main() function in auth-login.py')
    login_obj = Login()
    login_obj.load_conf()
    login_obj.req_get()
    login_obj.req_post()

    logging.info('finish login')


if __name__ == '__main__':
    """Run"""
    main()
