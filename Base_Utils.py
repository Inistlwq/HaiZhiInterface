# encoding: utf-8
"""
@author: cb_Lian 
@version: 1.0
@license: Apache Licence
@file: Base_Utils.py
@time: 2018/9/5 16:30
@Function：
"""
import talib
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
        self.prefix = "http://www.haizhilicai.com/"  # 公测地址
        # self.prefix = "http://192.168.0.136/"  # 内测地址
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
        if isinstance(temp_res, str):  # 考虑py2和py3中的字符串类型，py2中的str==bytes
            return temp_res
        elif isinstance(temp_res, bytes):
            temp_res = temp_res.decode()
            return temp_res


#  利用基本数据构造因子的类工具
class TechnicalIndicators(object):
    """技术类指标，目前包括MACD等"""
    def __init__(self):
        pass

    @staticmethod
    def MACD(single_stock_df, col='close', fastperiod=12, slowperiod=26, signalperiod=9):
        """
           计算macd的三种指标,一般来说fastperiod=12, slowperiod=26, signalperiod=9
           重要参数：close收盘价
        """
        single_stock_df['macd_diff'], single_stock_df['macd_dea'], single_stock_df['macd_histogram'] = talib.MACDEXT(
            single_stock_df[col], fastperiod=fastperiod, fastmatype=1, slowperiod=slowperiod, slowmatype=1,
            signalperiod=signalperiod, signalmatype=1)
        single_stock_df['macd_histogram'] *= 2
        return single_stock_df

    @staticmethod
    def MA(single_stock_df, col='close', timeperiod=5):
        """
        计算简单移动平均值，常用线有5天、10天、30天、60天、120天和240天的指标
        重要参数：close收盘价
        """
        single_stock_df["ma_%d" % timeperiod] = talib.MA(single_stock_df[col], timeperiod)
        return single_stock_df

    @staticmethod
    def EMA(single_stock_df, col='close', timeperiod=5):
        """
        计算指数移动平均值，常用线有5天、10天、30天、60天、120天和240天的指标
        重要参数：close收盘价
        """
        single_stock_df["ema_%d" % timeperiod] = talib.EMA(single_stock_df[col], timeperiod)
        return single_stock_df

    @staticmethod
    def MOM(single_stock_df, col='close', timeperiod=12):
        """
        计算动量，一般设置timeperiod为12日
        重要参数：close收盘价
        """
        single_stock_df["mom_%d" % timeperiod] = talib.MOM(single_stock_df[col], timeperiod)
        return single_stock_df

    @staticmethod
    def RSI(single_stock_df, col='close', timeperiod=6):
        """
        计算RSI:天数一般是6、12、24
        重要参数：close收盘价
        """
        single_stock_df["rsi_%d" % timeperiod] = talib.RSI(single_stock_df[col], timeperiod)
        return single_stock_df

    @staticmethod
    def Boll(single_stock_df, col='close', timeperiod=20, nbdevup=2, nbdevdn=2):
        """
        计算布林线，imeperiod=20, nbdevup=2, nbdevdn=2
        重要参数：close收盘价
        """
        single_stock_df["boll_%d_lower" % timeperiod], single_stock_df["boll_%d_mid" % timeperiod], \
            single_stock_df["boll_%d_upper" % timeperiod] = talib.BBANDS(single_stock_df[col],  timeperiod, nbdevup, nbdevdn)
        return single_stock_df

    @staticmethod
    def KDJ(single_stock_df, col_h='high', col_l='low', col_c='close', fastk_period=9, slowk_period=3, slowd_period=3):
        """
        计算kdj随机指标，fastk_period=9, slowk_period=3, slowd_period=3
        重要参数：high最高价 low最低价 close收盘价
        """
        single_stock_df['kdj_k'], single_stock_df['kdj_d'] = talib.STOCH(single_stock_df[col_h], single_stock_df[col_l],
                                                                         single_stock_df[col_c],
                                                                         fastk_period=fastk_period,
                                                                         slowk_period=slowk_period, slowk_matype=0,
                                                                         slowd_period=slowd_period, slowd_matype=0)
        single_stock_df['kdj_j']=single_stock_df['kdj_k'] * 3 - single_stock_df['kdj_d'] * 2
        return single_stock_df

    @staticmethod
    def WR(single_stock_df, col_h='high', col_l='low', col_c='close', timeperiod=10):
        """
        计算威廉指标，timeperiod=10
        重要参数：high最高价 low最低价 close收盘价,此处算出为负值需要取绝对值
        """
        single_stock_df['wr'] = talib.WILLR(single_stock_df[col_h], single_stock_df[col_l],single_stock_df[col_c],timeperiod=timeperiod)
        single_stock_df['wr'] = single_stock_df['wr'].abs()
        return single_stock_df

    @staticmethod
    def DMI(single_stock_df, col_h='high', col_l='low', col_c='close', timeperiod=14):
        """
        计算DMI指标(DI、MINUS_DI 、ADX、ADXR)，timeperiod=14
        重要参数：high最高价 low最低价 close收盘价,此处算出为负值需要取绝对值
        """
        single_stock_df['dmi_di'] = talib.DX(single_stock_df[col_h], single_stock_df[col_l],single_stock_df[col_c],timeperiod=timeperiod)
        single_stock_df['dmi_mdi'] = talib.MINUS_DI(single_stock_df[col_h], single_stock_df[col_l],
                                             single_stock_df[col_c], timeperiod=timeperiod)
        single_stock_df['dmi_adx'] = talib.ADX(single_stock_df[col_h], single_stock_df[col_l],
                                             single_stock_df[col_c], timeperiod=timeperiod)
        single_stock_df['dmi_adxr'] = talib.DX(single_stock_df[col_h], single_stock_df[col_l],
                                             single_stock_df[col_c], timeperiod=timeperiod)
        return single_stock_df

    @staticmethod
    def CCI(single_stock_df, col_h='high', col_l='low', col_c='close', timeperiod=6):
        """
        计算CCI指标 timeperiod=6 或 12
        重要参数：high最高价 low最低价 close收盘价,
        """
        single_stock_df['cci'] = talib.CCI(single_stock_df[col_h], single_stock_df[col_l], single_stock_df[col_c], timeperiod)
        return single_stock_df

    @staticmethod
    def ATR(single_stock_df, col_h='high', col_l='low', col_c='close', timeperiod=14):
        """
        计算均幅指标ATR timeperiod=14
        重要参数：high最高价 low最低价 close收盘价,
        """
        single_stock_df['atr'] = talib.ATR(single_stock_df[col_h], single_stock_df[col_l], single_stock_df[col_c],
                                           timeperiod)
        return single_stock_df
