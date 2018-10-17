# coding:utf-8
from .Base_Utils import BaseUtils
import time

class HaizhiData(BaseUtils):
    def __init__(self, userid, password):
        super(HaizhiData, self).__init__(userid, password)  # 使用super函数
        self.stock_encode_name = 'data'

    # 获取某个时期单只股票的某些属性
    def get_stock_args(self, code, startday="", endday="", args=[]):
        data_url = self.prefix + 'Tradeinterface/get_data'
        if startday == '':  # 未设置默认为'1990-12-19'
            return "startday can't be null"
        if endday == '':  # 未设置默认为今天日期
            return "endday can't be null"
        self.send_dic['code'] = code
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        self.send_dic['att'] = args
        return self.http_post(self.send_dic, self.stock_encode_name, data_url)

    # 获取某个时期所有股票的某个属性
    def get_stocks_arg(self, startday="", endday="", arg=""):
        stocks_arg_url = self.prefix + 'Tradeinterface/get_stocks_arg'
        if arg == '':
            return "arg can't be null"
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        self.send_dic['att'] = arg
        return self.http_post(self.send_dic, self.stock_encode_name, stocks_arg_url)

    # 获取某个时期沪市或深市的所有股票代码
    def get_exchange_stocks(self, startday="", endday="", exchange="all"):
        exchange_stocks_url = self.prefix + 'Tradeinterface/get_exchange_stocks'
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
        return self.http_post(self.send_dic, self.stock_encode_name, exchange_stocks_url)

    # 获取某个时期某个板块的所有股票代码
    def get_plate_stocks(self, startday="", endday="", plate=""):
        plate_stocks_url = self.prefix + 'Tradeinterface/get_plate_stocks'
        if plate == '':
            return "plate should only be a existed industry or concept or region"
        self.send_dic['plate'] = plate
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        return self.http_post(self.send_dic, self.stock_encode_name, plate_stocks_url)

    # 获取指数里历史数据，目前支持上证指数、深证成指、创业板指、上证50
    def get_index_data(self, startday="", endday="", index_name=''):
        # index_name取值只能为上证指数、深证成指、创业板指、上证50
        index_data_url = self.prefix + 'Tradeinterface/get_index_data'
        if startday == '':
            startday = '2010-01-04'
        if endday == '':
            endday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if index_name not in ['上证指数', '深证成指', '创业板指', '上证50']:
            return "index_name must be one of ['上证指数', '深证成指','创业板指','上证50']"
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        self.send_dic['index'] = index_name
        return self.http_post(self.send_dic, self.stock_encode_name, index_data_url)

