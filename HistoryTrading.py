# coding:utf-8
import os
import time
import pandas as pd
from .Base_Utils import BaseUtils


class HistoryTrading(BaseUtils):
    """
    参数说明: 1.userId，用户Id，需在海知平台注册获得，默认'',必须设置
              2.password，用户密码，海知平台注册时用户所设，默认'',必须设置
              3.code，买卖股票代码,必须设置
              4.volume，买卖数量，必须设置
              5.price，买卖的价格,在price_type 为limit_price时必须设置
              6.price_type，报价类型，取值为‘limit_price’、‘now_price’，必须设置
              7.effect_term，有效期限，取值为1,2,3…10，1代表今天，2代表明天，其他依此类推

    """

    def __init__(self, userid, password, strategy_name, type = ""):
        super(HistoryTrading, self).__init__(userid, password)  # 使用super函数
        self.send_dic['type'] = type
        self.stock_encode_name = 'tradeinfo'
        self.query_pro_encode_name = 'query_info'
        self.cancel_encode_name = 'cancel_info'
        self.strategy_name = strategy_name
        self.set_strategy_name(strategy_name)

    # 批量买卖交易
    def bt_batch_buy_sell(self):
        trade_url = self.prefix + 'Tradeinterface/bt_tradeinfo'
        return self.http_post(self.send_dic, self.stock_encode_name, trade_url)

    # 买交易
    def bt_buy(self):
        trade_url = self.prefix + 'Tradeinterface/bt_tradeinfo'
        self.send_dic['buy_sell_type'] = 'bt_buy'
        return self.http_post(self.send_dic, self.stock_encode_name, trade_url)

    # 卖交易
    def bt_sell(self):
        trade_url = self.prefix + 'Tradeinterface/bt_tradeinfo'
        self.send_dic['buy_sell_type'] = 'bt_sell'
        return self.http_post(self.send_dic, self.stock_encode_name, trade_url)

    # 资产和持仓情况
    def query_profit(self):
        prof_info_url = self.prefix + 'Tradeinterface/get_profit_info'
        return self.http_post(self.send_dic, self.query_pro_encode_name, self.prof_info_url)

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

    # 得到交割单的csv文件
    def get_history_csv(self, csv_path='', filename='交割单'):
        import json
        if not os.path.isdir(csv_path):
            return "path not exist!"  # 路径不存在

        data = self.bt_query_history_records(startday="", endday="")
        data = json.loads(data)
        if isinstance(data[0], int):  # 如果返回的是错误信息，直接返回
            return json.dumps(data)

        data = pd.DataFrame(data)  # 返回了交割单正常进行处理
        # 转换成交量与发生金额，有正负之分
        for idx in data.index:
            line = data.loc[idx]
            if line['trade_type'] == '3':  # 卖出成交量设为负
                line['Volume'] = '-'+line['Volume']
            if line['trade_type'] == '1':  # 买入发生金额设为负
                line['hap_fund'] = '-' + line['hap_fund']

        data = data[['timestamp', 'SecurityID', 'Symbol', 'trade_type', 'price_order', 'price_deal',
                     'Volume', 'fund_deal', 'fee', 'tax',
                     'other_fee', 'security_holding', 'hap_fund', 'remain_fund']]
        # 转换操作，中文买入卖出
        data['trade_type'] = data['trade_type'].apply(lambda x: '系统发放' if x == '6' else '买入' if x == '1' else '卖出')
        # 转换列表名
        data = data.rename(columns={'timestamp': '成交时间', 'SecurityID': '代码', 'Symbol': '名称', 'trade_type': '操作',
                                    'price_order': '委托价', 'price_deal': '成交价', 'Volume': '成交量', 'fund_deal': '成交金额',
                                     'fee': '手续费', 'tax': '印花税', 'other_fee': '其他杂费', 'security_holding': '证券余额',
                                    'hap_fund': '发生金额', 'remain_fund': '现金余额'})

        data.to_csv(csv_path+'/'+filename+'.csv', sep=",", index=False, encoding='gbk')

        return 'generate trade csv success!'

    # 历史交割
    def bt_query_history_records(self, startday="", endday=""):
        bt_get_history_url = self.prefix + 'Tradeinterface/bt_get_history_info'
        if startday == '':  # 未设置默认为'1990-12-19'
            startday = '1990-12-19'
        if endday == '':  # 未设置默认为今天日期
            endday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.send_dic['start_day'] = startday
        self.send_dic['end_day'] = endday
        return self.http_post(self.send_dic, self.query_pro_encode_name, bt_get_history_url)

    # 创建用户策略
    def create_strategy(self, strategy_name=''):
        create_strategy_url = self.prefix + 'Tradeinterface/create_strategy'
        self.send_dic['strategy_name'] = strategy_name
        return self.http_post(self.send_dic, self.query_pro_encode_name, create_strategy_url)

    # 根据用户策略名称查找策略id与用户id
    def get_uuid_strategy_id(self):
        get_uuid_strategy_id_url = self.prefix + 'Tradeinterface/get_uuid_strategy_id'
        res = self.http_post(self.send_dic, self.query_pro_encode_name, get_uuid_strategy_id_url)
        import json
        res = json.loads(res)
        if isinstance(res[0], int):
            return 'strategy not exist', 'strategy not exist'
        else:
            return res[0]['user_id'], res[0]['strategy_id']



    # 查看用户策略
    def get_strategy(self):
        get_strategy_url = self.prefix + 'Tradeinterface/get_strategy'
        return self.http_post(self.send_dic, self.query_pro_encode_name, get_strategy_url)

    # 删除用户策略
    def del_strategy(self, del_strategy_name=''):
        del_strategy_url = self.prefix + 'Tradeinterface/del_strategy'
        self.send_dic['del_strategy_name'] = del_strategy_name
        return self.http_post(self.send_dic, self.query_pro_encode_name, del_strategy_url)

    # 设置用户策略
    def set_strategy_name(self, strategy_name=''):
        strategy_name = str(strategy_name)
        if strategy_name.strip() != '':
            self.send_dic['strategy_name'] = strategy_name
            return True
        else:
            return False

    # 设置买卖股票列表
    def set_stock_dic(self, stock_dic=None, is_buy_sell_combine=False):
        if is_buy_sell_combine is True:  # 批量同时买卖模式，此时需要在stock_dic的每个dict中需额外加入cur_buy_sell_type属性标志当前股票是买还是卖
            if isinstance(stock_dic, list):
                for x in stock_dic:
                    if 'cur_buy_sell_type' not in x.keys():
                        return "AttributeError, in batch model,cur_buy_sell_type should be in each dict"
                self.send_dic['stock_dic'] = stock_dic
            else:
                return (TypeError, " in batch model,set_stock_dic function should use list as args ")
        else:  # 批量买 批量卖 独自买 独自卖模式
            if isinstance(stock_dic, list) or isinstance(stock_dic, dict):
                if len(stock_dic) > 0:
                    self.send_dic['stock_dic'] = stock_dic
                    return True
                else:
                    return False
            else:
                raise (TypeError, " set_stock_dic function should use list or dict as args")

    # 设置买卖股票列表模板
    @staticmethod
    def get_stock_dic():
        stock_dic = {'price_type': '', 'volume': '', 'code': '', 'date': ''}
        return stock_dic

    # 设置引擎的种类
    def set_engine_type(self, type):
        """
        :param type: 引擎种类，type=""为默认的历史回测引擎，type="today"为今日盘后总结引擎
        :return:
        """
        self.send_dic['type'] = type

