#coding=utf8
import itchat, time
import requests
from itchat.content import *


KEY = ''

@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    def get_response(msg):
        apiUrl = 'http://www.tuling123.com/openapi/api'
        data = {
            'key'    : KEY,
            'info'   : msg,
            'userid' : 'wechat-robot',
        }
        try:
            r = requests.post(apiUrl, data=data).json()
            return r.get('text')
        except:
            return

    defaultReply = u'你说的这句话：' + msg['Text'] + u'，我听不懂'
    reply = get_response(msg['Text']) + u' (发自小秘书)'
    return reply or defaultReply

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print 'PIC'
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    def get_response(msg):
        apiUrl = 'http://www.tuling123.com/openapi/api'
        data = {
            'key'    : KEY,
            'info'   : msg,
            'userid' : 'wechat-robot',
        }
        try:
            r = requests.post(apiUrl, data=data).json()
            return r.get('text')
        except:
            return

    if msg['User']['NickName'] == 'Group_Name' or msg['User']['NickName'] == 'Group_Name2':
        
        if msg['isAt']:
            #\u2005 is @ suffix
            itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'], u'找我什么事呀'), msg['FromUserName'])
        else:
            #You can get your user id from printing message, it's a long id
            if msg['FromUserName'] != Your_User_ID:
                responses = get_response(msg['Content'])
                msg.user.send(u'%s' % (responses))

#Auto login
itchat.auto_login(hotReload=True)
itchat.run()

