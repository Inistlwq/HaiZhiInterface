##海知程序化模拟交易接口的说明

海知平台现在推出了程序化模拟交易接口，方便用户利用计算机技术进行智能投资！接口使用python编写，请在python2.7以上的环境中运行接口（目前接口暂不支持python3）。接口是开源免费的，欢迎大家在使用过程中提出宝贵意见！！！目前接口仅支持股票交易，我们会陆续完善其他金融产品的交易功能！

附上海知接口的github地址：https://github.com/NotTodayNotMe/TradeInterface.git

####接口安装
```python
pip install TradeInterface
```
####接口说明
目前接口仅提供最简单的买卖交易以及交易信息查询功能，目的是给熟悉量化投资的用户充分的自由度，可以最大自由度的实现自己的投资策略。
```python
from TradeInterFace import TestEngine #导入接口

Engine = TestEngine(user_id = '',password = '',type = '')
'''
初始化测试引擎示例，必须选定是实盘模拟还是历史回测
parameter:
	#user_id:海知平台用户id（str）
	#password:(str)
	#type:
		RealTimeTrading:实盘模拟
		HistoryTrading:历史回测
'''
Engine.core#返回测试引擎类型，是实盘模拟还是历史回测
Engine.current_time#返回测试引擎的当前时间戳。实盘模拟返回当前时间，历史回测返回当前设定的历史时间
Engine.shift_current_time(days = )#按照天数变更当前的引擎时间戳,仅对历史回测有效，同时仅支持向后跳转！目的是标准化历史回测的过程，防止用现在的数据在过去的时间购买股票！
Engine.buy(code = '',#股票代码
		   volume = '',#交易量
		   price_type = 'now_price',#价格类型
		   price =None,#价格
		   date = None,#交易时间，近在历史回测引擎时生效，为空时默认使用当前的引擎时间戳
		   effect_term = 1)#挂单有效时长
Engine.sell(code = '',#股票代码
		   volume = '',#交易量
		   price_type = 'now_price',#价格类型
		   price =None,#价格
		   date = None,#交易时间，近在历史回测引擎时生效，为空时默认使用当前的引擎时间戳
		   effect_term = 1)#挂单有效时长
Engine.query_records(start = '',end ='')#查询委托交易情况，仅实盘模拟有效
Engine.cancel_order(pre_id = )#根据委托单号撤单，仅实盘模拟有效
Engine.query_history_records(start = ,end = '')#查询历史交割单
Engine.history_to_csv(path = )#将历史交割单输出到csv文件当中
#设定引擎时间戳是为了方便历史回测和实盘模拟直接的切换
#对于用户已经编辑好的策略，想在实盘模拟和历史投资之间切换，只需要修改引擎的初始化参数即可

```
####使用样例
```pyhton
user_id ='******'
password = '******'
def Realtime():
    '''
    实盘交易引擎使用样例
    :return:
    '''
    Engine = TestEngine(user_id=user_id,password=password,type='RealTimeTrading')#初始化接口，传入登录信息，选择实盘模拟
    print Engine.core
    print Engine.current_time
    print Engine.buy(code='600848',volume=100)#购买
    print Engine.sell(code='600848', volume=100)#卖出
    temp = Engine.query_records(start="2018-04-25", end="2018-04-26")#委托查询，主要是用来查询委托单号
    print temp[0]['pre_id']#返回最后的委托
    print Engine.cancel_order(str(temp[0]['pre_id']))#撤销委托单，需要传入委托单好
    print Engine.query_history_records(start="2018-4-4", end="2018-04-05")#查看历史交易记录
    print Engine.query_profit()#收益情况查询
'''历史回测引擎示例'''
def History():
    '''
    历史回测引擎
    :return:
    '''
    Engine = TestEngine(user_id=user_id,password=password,type='HistoryTrading')
    print Engine.core
    print Engine.current_time
    print Engine.list_stratagy()#显示当前历史回测引擎当中存储的交易策略
    if Engine.list_stratagy():
        '''
        对于历史回测，需要在运行的时候指定一个回测策略。最简单的方式就是创建一个新的策略然后直接指定该策略。
        '''
        Engine.del_stratagy(Engine.list_stratagy()[0]['strategy_name'])#删除策略
        Engine.create_stratagy(user_id)#创建新策略
        Engine.set_stratagy(user_id)#将回测引擎指定为该策略
    else:
        Engine.create_stratagy(user_id)
        Engine.set_stratagy(user_id)
    print Engine.buy(code =600848,volume=1000,date = '2017-10-11')
    Engine.current_time = '2018-4-8'#制定历史回测引擎的交易日期
    Engine.shift_current_time(1)#将历史回测引擎的交易日期向后跳转一天
    print Engine.current_time
    print Engine.sell(code='600848',volume=100)
    print Engine.history_to_csv('history')#将交割单输出到csv文件，需要传入存储csv文件的文件夹名，在
                                          #本例子中，导入接口的项目下有一个名为history的文件夹，否则会提示路径不存在


if __name__ == '__main__':
    Realtime()
    History()

```
####注意事项

1.接口不支持python3！！！！！

2.接口现在仅提供最简单的交易方法和交易情况的查询方法，目的是给用户充分的自由度实现自己的策略

3.对于新手用户，接口目前可能不够友好，在实现自己的策略时，可能会出现很多问题，我们还提供了一套功能更加完善，更加傻瓜的模拟系统

附上github地址：https://github.com/NotTodayNotMe/Fintech.git

模拟系统是开源的，欢迎大家使用并提出宝贵意见！
