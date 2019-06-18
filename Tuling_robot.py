import requests
import itchat

#图灵机器人的api key
KEY = '746bb978bcd840258163d29530586c9c'

def get_response(msg):
    #这里实现与图灵机器人的交互
    #构造了要发送给服务器的数据
    api_url = 'http://www.tuling123.com/openapi/api'#链接
    data = {
        'key':KEY,
        'info':msg,
        'userid':'wechat-robot',
        }
    try:
        r = requests.post(api_url,data=data).json()
        #字典的get方法在字典里没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    #异常处理机制
    except:
        #遇到异常，返回None
        return

#这里实现微信消息的获取
@itchat.msg_register(itchat.content.TEXT)

def tuling_reply(msg):
    reply = '[自动回复]' + get_response(msg['Text'])
    #将图灵机器人的回复打印在屏幕上
    print(reply)
    #保证在KEY出问题时可以使用默认的回复方式
    defaultReply = '[自动回复]'+'I received:' + msg['Text']
    #利用'或'语句的'偷懒'
    #如果reply不为空，回复reply内容，否则，按照默认方式回复
    return reply or defaultReply

if __name__ == "__main__":
	#热启动，多次运行程序时，不需要多次扫码
	itchat.auto_login(hotReload=True)
	itchat.run()
