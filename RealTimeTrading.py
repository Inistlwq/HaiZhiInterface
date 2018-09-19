# coding:utf-8

from .Base_Utils import BaseUtils


class RealTimeTrading(BaseUtils):
    """
    参数说明: 1.userId，用户Id，需在海知平台注册获得，默认'',必须设置
              2.password，用户密码，海知平台注册时用户所设，默认'',必须设置
              3.code，买卖股票代码,必须设置
              4.volume，买卖数量，必须设置
              5.price，买卖的价格,在price_type 为limit_price时必须设置
              6.price_type，报价类型，取值为‘limit_price’、‘now_price’，必须设置
              7.effect_term，有效期限，取值为1,2,3…10，1代表今天，2代表明天，其他依此类推

    """

    def __init__(self, userid, password):
        super(RealTimeTrading, self).__init__(userid, password)
        self.stock_encode_name = 'tradeinfo'
        self.query_pro_encode_name = 'query_info'
        self.cancel_encode_name = 'cancel_info'
        # self.send_dic = {'userid': '', 'password': '', 'buy_sell_type': '', 'stock_dic': {}}

    # 买交易
    def buy(self):
        trade_url = self.prefix + 'Tradeinterface/get_tradeinfo'
        self.send_dic['buy_sell_type'] = 'buy'
        return self.http_post(self.send_dic, self.stock_encode_name, trade_url)

    # 卖交易
    def sell(self):
        trade_url = self.prefix + 'Tradeinterface/get_tradeinfo'
        self.send_dic['buy_sell_type'] = 'sell'
        return self.http_post(self.send_dic, self.stock_encode_name, trade_url)

    # 资产和持仓情况
    def query_profit(self):
        prof_info_url = self.prefix + 'Tradeinterface/get_profit_info'
        return self.http_post(self.send_dic, self.query_pro_encode_name, prof_info_url)

    # 委托记录
    def query_records(self, startday="", endday=""):
        query_records_url = self.prefix + 'Tradeinterface/get_rocords_info'
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        return self.http_post(self.send_dic, self.query_pro_encode_name, query_records_url)

    # 撤单
    def cancel_order(self, pre_id=""):
        cancel_url = self.prefix + 'Tradeinterface/cancel_orders'
        self.send_dic['pre_id'] = pre_id
        return self.http_post(self.send_dic, self.cancel_encode_name, cancel_url)

    # 历史交割
    def query_history_records(self, startday="", endday=""):
        query_history_url = self.prefix + 'Tradeinterface/get_history_info'
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        return self.http_post(self.send_dic, self.query_pro_encode_name, query_history_url)

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