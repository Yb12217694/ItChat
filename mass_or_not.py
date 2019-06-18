#导入itchat和time
import itchat
import time
#设置计数器
count = 1

def send_msg():
    #获取好友列表
    friends_list = itchat.get_friends(update = True)
    #是否群发
    ismass = input('Whether it is mass (Yes or No) : ')
    if ismass == 'Yes':
        #索取需要群发的消息
        mass_msg = input('Please enter the message you want to send in bulk : ')
        #对列表中好友进行群发
        for friend in friends_list:
            toFriend = friend['UserName']
            itchat.send(mass_msg,toFriend)
            time.sleep(1)#每发送一次暂停一秒(防冻结帐号)
    else:
        #单独发送,索取收消息人的备注、待发送的消息内容、重复发送次数
        ps = input('Please enter a friend note : ')
        msg = input('Please enter the message you want to send : ')
        times = eval(input('Please enter the number of times sent : '))
        #在已获取的好友列表中查找到收消息人的'UserName'
        name = itchat.search_friends(name = ps)
        toName = name[0]['UserName']
        #根据重复发送次数进行重复发送,不足一次的按照一次计算
        if times <= 1:
            itchat.send(msg,toName)
            print('Has been sent!')
        else:
            for i in range(times):
                itchat.send(msg,toName)
                print('Sent %d times!' % (i+1))
                time.sleep(0.001 * (times - i) + 1)#每发送一次暂停一下

if __name__ == '__main__':
    itchat.auto_login()#手机扫码登录
    #循环调用send_msg()函数
    while True:
        print('Round %d' % count)
        send_msg()
        count = count + 1
