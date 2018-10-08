# encoding: utf-8
"""
@author: cb_Lian 
@version: 1.0
@license: Apache Licence
@file: Base_Utils.py
@time: 2018/9/5 16:30
@Function：
"""
import json
import hashlib
import platform
if platform.python_version() > '3.0':
    import urllib.parse as urlencode
    import urllib.request as request
    import urllib.request as urlopen
else:
    import urllib as urlencode
    import urllib2 as request
    import urllib2 as urlopen


# 基本的工具类，便于其他几个类继承
class BaseUtils(object):
    def __init__(self, userid, password):
        # self.prefix = "http://www.haizhilicai.com/"  # 公测地址
        self.prefix = "http://192.168.0.136/"  # 内测地址
        self.send_dic = {'userid': '', 'password': ''}
        self.set_userid(userid)
        self.set_password(password)

    # 验证用户信息是否正确
    def vali_usr_info(self):
        vali_url = self.prefix + 'Tradeinterface/vali_usr_info'
        stock_encode_name = 'usr_info'
        return self.http_post(self.send_dic, stock_encode_name, vali_url)

    # 设置用户id
    def set_userid(self, userid=''):
        userid = str(userid)
        if userid.strip() != '':
            self.send_dic['userid'] = userid
            return True
        else:
            return False
        # 设置用户密码

    # 设置用户密码
    def set_password(self, password=''):
        password = str(password)
        if password.strip() != '':
            self.send_dic['password'] = self.md5encryption(password)
            return True
        else:
            return False

    # 实现md5加密
    @staticmethod
    def md5encryption(password):
        if password.strip() != '':
            md = hashlib.md5()
            md.update(password.encode("utf8"))
            return md.hexdigest()
        else:
            return ''

    # 向服务器发送请求
    @staticmethod
    def http_post(send_dic, urlencode_name, url):
        jdata = json.dumps(send_dic)  # json格式化编码
        jdata = urlencode.urlencode({urlencode_name: jdata}).encode(encoding='utf8')  # urlencode编码
        req = request.Request(url, jdata)  # 生成页面请求的完整数据
        res = urlopen.urlopen(req)  # 发送页面请求
        temp_res = res.read()  # 返回结果，把list结果处理为字符串显示
        return temp_res
