#coding:utf-8
import os
import time
import json
import urllib2
import urllib
import hashlib
import sys
import pandas as pd

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class RealTimeTrading(object):
    """
    参数说明: 1.userId，用户Id，需在海知平台注册获得，默认'',必须设置
              2.password，用户密码，海知平台注册时用户所设，默认'',必须设置
              3.code，买卖股票代码,必须设置
              4.volume，买卖数量，必须设置
              5.price，买卖的价格,在price_type 为limit_price时必须设置
              6.price_type，报价类型，取值为‘limit_price’、‘now_price’，必须设置
              7.effect_term，有效期限，取值为1,2,3…10，1代表今天，2代表明天，其他依此类推

    """

    def __init__(self, userid='', password=''):
        self.prefix = "http://www.haizhilicai.com/"
        self.trade_url = self.prefix + 'Tradeinterface/get_tradeinfo'
        self.prof_info_url = self.prefix + 'Tradeinterface/get_profit_info'
        self.query_records_url = self.prefix + 'Tradeinterface/get_rocords_info'
        self.cancel_url = self.prefix + 'Tradeinterface/cancel_orders'
        self.query_history_url = self.prefix + 'Tradeinterface/get_history_info'
        self.stock_encode_name = 'tradeinfo'
        self.query_pro_encode_name = 'query_info'
        self.cancel_encode_name = 'cancel_info'
        self.send_dic = {'userid': '', 'password': '', 'buy_sell_type': '', 'stock_dic': {}}
        self.set_userid(userid)
        self.set_password(password)

    # 买交易
    def buy(self):
        self.send_dic['buy_sell_type'] = 'buy'
        return self.http_post(self.send_dic, self.stock_encode_name, self.trade_url)

    # 卖交易
    def sell(self):
        self.send_dic['buy_sell_type'] = 'sell'
        return self.http_post(self.send_dic, self.stock_encode_name, self.trade_url)

    # 资产和持仓情况
    def query_profit(self):
        return self.http_post(self.send_dic, self.query_pro_encode_name, self.prof_info_url)

    # 委托记录
    def query_records(self, startday="", endday=""):
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        return self.http_post(self.send_dic, self.query_pro_encode_name, self.query_records_url)

    # 撤单
    def cancel_order(self, pre_id=""):
        self.send_dic['pre_id'] = pre_id
        return self.http_post(self.send_dic, self.cancel_encode_name, self.cancel_url)

    # 历史交割
    def query_history_records(self, startday="", endday=""):
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        return self.http_post(self.send_dic, self.query_pro_encode_name, self.query_history_url)

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

    # 设置买卖股票列表
    def set_stock_dic(self, stock_dic={}):
        if len(stock_dic) > 0:
            self.send_dic['stock_dic'] = stock_dic
            return True
        else:
            return False

    # 设置买卖股票列表模板
    @staticmethod
    def get_stock_dic():
        stock_dic = {'price': '', 'price_type': '', 'effect_term': '', 'volume': '', 'code': ''}
        return stock_dic

    # 实现md5加密
    @staticmethod
    def md5encryption(password):
        if password.strip() != '':
            md = hashlib.md5()
            md.update(password)
            return md.hexdigest()
        else:
            return ''

    # 发起交易请求
    @staticmethod
    def http_post(send_dic, urlencode_name, url):
        jdata = json.dumps(send_dic)  # json格式化编码
        # print(jdata)
        # exit()
        jdata = urllib.urlencode({urlencode_name: jdata})  # urlencode编码
        req = urllib2.Request(url, jdata)  # 生成页面请求的完整数据
        res = urllib2.urlopen(req)  # 发送页面请求
        temp_res = res.read()  # 返回结果，把list结果处理为字符串显示
        return temp_res

