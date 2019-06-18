from tkinter import *
from PIL import Image
from PIL import ImageTk
import itchat
import requests
import time
from itchat.content import *
from AutoReply import *  #自定义模块

isFriend = False

def to_friend():
    msg = msg_entry.get()  #获取消息内容
    times = times_entry.get()#获取发送次数
    ps = to_entry.get()    #获取收件人备注

    msg_entry.delete(0,END)  #清空消息框
    times_entry.delete(0,END)
    #不擦除收件人备注

    for key in friends_dic.keys():
        #如果输入的好友名在字典中被查找到存在或有相关名字，记录下该键值对
        if ps in key:
            ps = key
            toName = friends_dic[key]
            break
    #未输入好友备注
    if ps == '':
        print("Please enter your friend's note correctly !")
    #根据重复发送次数进行重复发送,未填写次数或不足一次的按照一次计算
    elif times == '' or eval(times) <= 1:
        try:
            itchat.send(msg,toName)
            print('Has been sent!')
        except:#没有找到该好友
            print('Did not find the friend !')
    else:
        times = eval(times)
        for i in range(times):
            itchat.send(msg,toName)
            print('Sent %d times!' % (i+1))
            time.sleep(0.001 * (times - i) + 1)#每发送一次暂停一下
        else:
            print('{} has received {} messages from you !'.format(ps,times))
    print('Has responded to <{}>.Content is >>>{}'.format(ps,msg))

def to_group():
    msg = msg_entry.get()  #获取消息内容
    times = times_entry.get()
    group = to_entry.get()    #获取收件群聊名
    
    msg_entry.delete(0,END)  #清空消息框
    times_entry.delete(0,END)
    #不擦除收件群聊名
    #查找该群或相关群，记录下键值对
    for key in group_dic.keys():
        if group in key:
            group = key
            toGroup = group_dic[key]
            break
    try:
        times = eval(times)
        if group == '':     #未输入群聊名称
            print("Please enter the group you want to send correctly !")
        elif times == '' or times <= 0:
            itchat.send(msg,toGroup)   #发送消息
        else:
            for i in range(times):
                itchat.send(msg,toGroup)   #发送消息
                print('Sent %d times!' % (i+1))
                time.sleep(1)
        print("Successfully sent a message to the <{}> group !\nContent is >>>{}".format(group,msg))#发送成功，打印提示
    except:#没有找到该群
        print('Did not find the group !')
#复选框判断
def checkbutton():
    global isFriend
    isFriend = not isFriend
    
#判断到底发给好友还是发给群
def send_to():
    if isFriend:
        to_friend()
    else:
        to_group()
        
#进行群发 or 自动回复
def to_list():
    msg = msg_entry.get()  #获取消息内容
    ps = to_entry.get()
    msg_entry.delete(0,END)  #清空消息框
    times_entry.delete(0,END)

    #如果备注栏不为空，视为误操作，不进行群发
    if ps != '':
        print("Please empty the remarks column first !")
    elif msg == '':       #检测到无可发送消息，进入自动回复
        auto()
    else:               #存在可发送消息，群发
        for key in friends_dic.keys():
            toName = friends_dic['UserName']
            name = key
            itchat.send(msg,toName)#发送消息
            print("{} has received your message !".format(name))
            time.sleep(1)
        else:
            print("The message with content {} has completed mass sending".format(msg))

#获取头像
def get_HeadImg():
    My = itchat.get_friends(update = True)[0]#找到自己的位置
    img = itchat.get_head_img(userName = My['UserName'])
    #头像保存在程序当前目录下
    headImage = open("head.jpg",'wb')
    headImage.write(img)
    headImage.close()
    #缩小头像
    img = Image.open("head.jpg")
    new_img = img.resize((200,200),Image.BILINEAR)
    new_img.save('headImage.jpg')
    
def friendName():
    #打印好友在通讯录中的姓名
    for key in friends_dic.keys():
        print(key)
    print()

def groupName():
    #打印保存到通讯录的群名
    for key in group_dic.keys():
        print(key)
    print()

def getName():
    if isFriend:
        friendName()
    else:
        groupName()

#判断是否为表情图
def isEmoji(str):
    if u"\U0001F600" <= str and str <= u"\U0001F64F":
        return True
    elif u"\U0001F300" <= str and str <= u"\U0001F5FF":
        return True
    elif u"\U0001F680" <= str and str <= u"\U0001F6FF":
        return True
    elif u"\U0001F1E0" <= str and str <= u"\U0001F1FF":
        return True
    else:
        return False

friends_dic = {}#储存好友的'UserName'
def friends_list():
    #获取好友列表
    friends_list = itchat.get_friends(update = True)
    print("\nWhen the friend information is loading, please wait !\n... ...")
    for friend in friends_list:
        name = ''
        #拆解备注或昵称
        for f in friend['RemarkName'] or friend['NickName']:
            if isEmoji(f) == False:#非emoji
                name = name + f
        friends_dic[name] = friend['UserName']#增加键值对，构建好友字典

group_dic = {} #群聊字典,用于储存'UserName'
def group_list():
    #获取群聊列表
    group_list = itchat.get_chatrooms(update = True)
    print('Group chat information loading, please wait !\n... ...')
    #构建群聊的字典
    for group in group_list:
        chatroom = ''
        for g in group['NickName']:
            if isEmoji(g) == False:   #排除emoji
                chatroom = chatroom + g
        group_dic[chatroom] = group['UserName']
    print("Loading completed !\n")

def login():
    itchat.auto_login(hotReload = True)

def logout():
    itchat.logout()
    print("Successfully logged out !")
    tk.destroy()

def auto():
    print('Get ready for automatic reply !')
    auto_reply()
    tk.destroy()#退出手动回复

'''
#图灵机器人的 api key
KEY = '746bb978bcd840258163d29530586c9c'
'''
'''
              微信
    msg        __      HeadImage
    times      __
    send to    __
    checkButton (发送给个人还是群)     Sendit||groupit * Mass it * getName
'''
tk = Tk()
var = IntVar


if __name__ == '__main__':
    login()  #登录
    get_HeadImg()#获取头像
    friends_list()#准备好友字典
    group_list() #准备群聊的字典
    


tk.title('WeChat')#窗口标题
Label(tk,text = 'WeChat',width = 50).grid(row = 0,column = 0,sticky = 'e')#标题栏

out_btn = Button(tk,text = 'logout',width = 10,command = logout)#注销登录
out_btn.grid(row = 0,column = 2,sticky = 'ne')

signature = itchat.get_friends(update = True)[0]['Signature']
if signature != '':
    #放置个性签名
    Label(tk,text = 'My signature : ' + signature).grid(row = 1)
else:
    Label(tk).grid(row = 1)#空行
#提示输入需要发送的信息
msg_label = Label(tk,text = 'Please enter the message to send : ',width = 50)
msg_label.grid(row = 2,column = 0)

#输入需要发送的信息
msg_entry = Entry(tk,width = 50)
msg_entry.grid(row = 3,column = 0)

Label(tk).grid(row = 4)#空行

#提示输入发送次数
times_label = Label(tk,text = 'Please enter the number of times you need to send : ',width = 50)
times_label.grid(row = 5,column = 0)

#输入信息的发送次数
times_entry = Entry(tk,width = 50)
times_entry.grid(row = 6,column = 0)

Label(tk).grid(row = 7)#空行

#收件人或收件群
to_label = Label(tk,text = 'Send to : ',width = 50)
to_label.grid(row = 8,column = 0)

#输入收件人或收件群
to_entry = Entry(tk,width = 50)
to_entry.grid(row = 9,column = 0)

#复选框，不勾选->发给群,勾选->发给好友
Checkbutton(tk,text = "Send it to the friend",width = 20,variable = var,command = checkbutton).grid(row = 10,column = 0,sticky = 'W')
   
#放置微信头像
photo = Image.open('headImage.jpg')
photo = ImageTk.PhotoImage(photo)
label = Label(image = photo)
label.image = photo
label.grid(row = 1,column = 1,rowspan = 8,columnspan = 3,sticky = 'W'+'E'+'N'+'S',padx = 5,pady = 5)
        
#发送到好友或群
to_btn = Button(tk,text = 'Send it !',width = 20,command = send_to)
to_btn.grid(row = 9,column = 1)

#获得相应的好友列表或群聊列表名称
name_btn = Button(tk,text = 'Get list name',width = 20,command = getName)
name_btn.grid(row = 9,column = 2)

#群发
mass_btn = Button(tk,text = 'Bulk to send it'+' '*4+'|'+' '*4+'Automatic Response',width = 42,command = to_list)
mass_btn.grid(row = 10,column = 1,columnspan = 2)

#事件主循环
tk.mainloop()
