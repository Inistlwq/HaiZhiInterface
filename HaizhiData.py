#coding:utf-8
import json
import urllib2
import urllib
import hashlib
import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class HaizhiData(object):
    def __init__(self, userid='', password=''):
        self.prefix = "http://www.haizhilicai.com/"
        self.data_url = self.prefix + 'Tradeinterface/get_data'
        self.stocks_arg_url = self.prefix + 'Tradeinterface/get_stocks_arg'
        self.exchange_stocks_url = self.prefix + 'Tradeinterface/get_exchange_stocks'
        self.plate_stocks_url = self.prefix + 'Tradeinterface/get_plate_stocks'
        self.stock_encode_name = 'data'
        self.send_dic = {'userid': '', 'password': ''}
        self.set_userid(userid)
        self.set_password(password)

    # 设置用户id
    def set_userid(self, userid=''):
        userid = str(userid)
        if userid.strip() != '':
            self.send_dic['userid'] = userid
            return True
        else:
            return False
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
            md.update(password)
            return md.hexdigest()
        else:
            return ''

    # 获取某个时期单只股票的某些属性
    def get_stock_args(self, code, startday="", endday="", args=[]):
        if startday == '':  # 未设置默认为'1990-12-19'
            return "startday can't be null"
        if endday == '':  # 未设置默认为今天日期
            return "endday can't be null"
        self.send_dic['code'] = code
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        self.send_dic['att'] = args
        return self.http_post(self.send_dic, self.stock_encode_name, self.data_url)

    # 获取某个时期所有股票的某个属性
    def get_stocks_arg(self, startday="", endday="", arg=""):
        if arg == '':
            return "arg can't be null"
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        self.send_dic['att'] = arg
        return self.http_post(self.send_dic, self.stock_encode_name, self.stocks_arg_url)

    # 获取某个时期沪市或深市的所有股票代码
    def get_exchange_stocks(self, startday="", endday="", exchange="all"):
        if exchange == 'sh':
            exchange = '3'
        elif exchange == 'sz':
            exchange = '2'
        elif exchange == 'all':
            pass
        else:
            return "exchange should only be sh or sz or all"
        self.send_dic['exchange'] = exchange
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        return self.http_post(self.send_dic, self.stock_encode_name, self.exchange_stocks_url)

    # 获取某个时期某个板块的所有股票代码
    def get_plate_stocks(self, startday="", endday="", plate=""):
        if plate == '':
            return "plate should only be a existed industry or concept or region"
        self.send_dic['plate'] = plate
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        return self.http_post(self.send_dic, self.stock_encode_name, self.plate_stocks_url)
    @staticmethod
    def http_post(send_dic, urlencode_name, url):
        jdata = json.dumps(send_dic)  # json格式化编码
        jdata = urllib.urlencode({urlencode_name: jdata})  # urlencode编码
        req = urllib2.Request(url, jdata)  # 生成页面请求的完整数据
        res = urllib2.urlopen(req)  # 发送页面请求
        temp_res = res.read()  # 返回结果，把list结果处理为字符串显示
        return temp_res

