import itchat
import requests
import time
from itchat.content import *
import os

#图灵机器人的 api key
KEY = '62751eaf1ce34e8bab330b88495fa3fd'
def tuling_reply(msg):
    #这里实现与图灵机器人的交互
    #构造了要发送给服务器的数据
    api_url = 'http://www.tuling123.com/openapi/api'#链接
    data = {
        'key' : KEY,
        'info' : msg,
        'userid' : 'wechat_bot',
        }
    try:
        r = requests.post(api_url,data = data).json()
        #字典的get方法在字典里没有'text'值的时候会返回None,而不会抛出异常
        return r.get('text')
    #异常处理
    except:
        #遇到异常，返回None
        return

#分析接收的消息[消息发送时间,消息发送人,消息的类别]，并打印到屏幕上
def receive_msg(msg):
    global msg_from
    #收到消息的时间,发消息人的备注,消息类型
    msg_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    msg_from = (itchat.search_friends(userName = msg['FromUserName']))['RemarkName']
    msg_type = msg['Type']
    #将收到的消息打印在屏幕上
    print('{} \n<{}>向您发送了类型为{}的消息:\n>>>{}<<<\n '.format(msg_time,msg_from,msg_type,msg['Text']))
    #文本类消息由Tuling-robot自动回复
    if msg_type == 'Text':
        return tuling_reply(msg['Text']) + '\n'
    #音频、图片类消息,希望对方改为文本
    elif msg_type == 'Recording' or msg_type == 'Video' or msg_type == 'Picture':
        return "Sorry,I can't understand it.\nCan you send a text message?\n"
    #名片、附件及分享类消息,对对方表示感谢
    elif msg_type == 'Sharing' or msg_type == 'Card':
        return 'Thank you for your sharing.\n'
    #其他消息,告知对方忙碌中,不便于回复
    else:
        return "Sorry,I'm too busy to reply you in time.\n"

#接收的消息有文本,图片,位置,名片,分享,语音,附件,视频
@itchat.msg_register([TEXT,PICTURE,MAP,CARD,SHARING,RECORDING,ATTACHMENT,VIDEO])
def auto_reply(msg):
    reply = '[AutoReply]' + receive_msg(msg)
    print('Has responded to <{}>.Content is >>>{}'.format(msg_from,reply))
    #防止reply出现问题
    defaultReply = '[AutoReply]' + 'I received it!\n'
    #利用or逻辑短路
    return reply or defaultReply

cnt = 0
def auto_reply():
    #itchat.auto_login(hotReload = True) #以模块形式调用时不需要登录语句
    itchat.run()

if __name__ == '__main__':
    auto_reply()
