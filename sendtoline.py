import requests
import time
import random

class SendToLine: #完成版
    '''
    Ver 1.3 05/21
    SendToLineクラス
    インスタンス化する際に引数で登録してある名前を入力(現在kazukiのみ)、また省略可(デフォルトはkazuki)
    使用可能なメソッド
    .msg(msg), .img(msg, img), .stk(msg, feeling)   /   .on(), .off()
    それぞれテキストのみ、画像とテキスト、スタンプとテキストを送信 on/offメソッドで全てのインスタンスで送信をする/しないの切り替えができる(初期値はon)
    なおスタンプは現在2種('high', 'low')から選べる

    またpublicなインスタンス変数であり、変更も想定しているものとして
    self.msg_size_limit(初期800), self.package_id(初期1) を用意

    privateなインスタンス変数としてself._noticeを用意
    不具合が起きた時に、LINEへ送る最後の分に注意書きを追加する
    必要に応じてself._noticeに注意書きを追加する箇所を増やしていく
    '''
    __URL = 'https://notify-api.line.me/api/notify'

    def __init__(self, val = 'test'):
        self.user_dict = {
            'kazuki':'qr2GkZz25XUfmtICQVJe6Vlw9K7rcTSaBhoJk4qFfRx',
            'fx':'G3Vj0lpjMOJ14RXWuSaiqhDhlTdb0X4p834aJifZr8U',
            'renban':'dXFeSJ3lZdP6noZqKQKPSedo2xCeBLNLwa2HmPyVEZN',
            'test':'ISEvrT7lZpPYCamFxqOQ7gDH17bHQW4lUBTIWz2aigs',
            'marina':'SYARJFQJiVGL4E0MHj5eVdZGz9hhUlkQQQ5zQvFh9VV',
            'health_check':'VNVZ55rtEGPmCkOqpIDFsVp0l21C8Lqb3vWSHgo1lbd',
            'kashiwa_health_check':'BSFdzZ65e3p8x0OjJGnrtflcMim9LKmYiizqsx2QqDf',
        }
        self.stk_dict = {'high':{0:{1:10},1:{1:12},2:{2:40}},'low':{0:{1:8},1:{1:113},2:{2:43}}}
        if val in self.user_dict.keys():
            self.username = val
            self._access_token = self.user_dict[val]
        else:
            print('We cannot find the user named ' + val +'.')
            self.username = ''
            self._access_token = ''
        self.msg_size_limit = 800
        self._notice = ''
        self._switch = 'on'
    def __str__(self):
        user = ''
        i = 0
        for key in self.user_dict.keys():
            if i == 0:
                user += ' "'+key+'"'
            else:
                user += ' "'+key+'" '
            i += 1
        feel = ''
        i = 0
        for key in self.stk_dict.keys():
            if i == 0:
                feel += ' "'+key+'"'
            else:
                feel += ' "'+key+'" '
            i += 1
        text = '\n***SendToLine使い方***\n'\
            'メッセージ送信：.msg(text), .stk(text,feeling), .msg_test(text)\n'\
            'feelingには' +feel+ 'の' +str(i)+ '種類が選べます。\n'\
            'その他のメソッド：.on(), .off(), .test_mode(), .toggle_user(user)\n'\
            'userには' +user+ 'が登録されています\n'\
            '現在のユーザー：' +self.username+ '\n'
        return text

    def send(self, msg , img = None, feeling = None):
        headers = {'Authorization': 'Bearer ' + self._access_token}
        if self.msg_size_limit > 1000:
            self.msg_size_limit = 1000
        msg_length = len(msg)
        if msg == None or msg == '':
            msg = '\n'

        while msg_length > self.msg_size_limit :
            sendmsg = msg[:self.msg_size_limit]
            msg = '\n' + msg[self.msg_size_limit:]
            payload = {'message': sendmsg}
            if self._switch == 'off':
                return
            r = requests.post(self.__URL, headers=headers, params=payload,)
            time.sleep(1)
            msg_length -= self.msg_size_limit + 2

        payload = {}
        print(self._notice)
        if feeling != None:
            package_id,id = self._stk_random(feeling)
            payload['stickerPackageId'] = package_id
            payload['stickerId'] = id

        if img != None:
            if 'http' in img:
                img_on = requests.get(img).content
            else:
                try:
                    with open(img, 'rb') as this:
                        img_on = this
                except:
                    img_on = None
                    _notice += '\nimgに値が代入されましたが開けませんでした'
        else:
            img_on = None
        files = {'imageFile': img_on}

        payload['message'] = msg + self._notice

        if self._switch == 'off':
            return
        r = requests.post(self.__URL, headers=headers, params=payload, files=files)

    def msg(self, msg):
        self.send(msg)
    def img(self, msg, img):
        self.send(msg, img)
    def stk(self, msg, feeling):
        self.send(msg, None, feeling)
    def off(self):
        self._switch = 'off'
        print('sendline:メッセージが送信不可能になりました')
    def on(self):
        self._switch = 'on'
        print('sendline:メッセージが送信可能になりました')

    def _stk_random(self, feeling):
        try:
            tag = random.choice(list(self.stk_dict[feeling].values()))
            for a,b in tag.items():
                package_id,id = a,b
            return package_id,id
        except:
            self._notice = self._notice + '\n※スタンプを指定するキーワードが正しく入力されませんでした'
            return 1, 101

    def test_mode(self):
        id = 'test'
        self.username = id
        self._access_token = self.user_dict[id]
        print('sendline:userを"test"に変更しました')
    def msg_test(self,text):
        val = self._access_token
        self._access_token = self.user_dict['test']
        self.msg(text)
        self._access_token = val
    def toggle_user(self,user):
        self.username = user
        self._access_token = self.user_dict[user]
        print('sendline:userを"'+user+'"に変更しました')

if __name__ == "__main__":
    test = SendToLine('test')
    print(test)
    test.off()
    test.on()
    test.test_mode()
    test.toggle_user('test')
    test.msg('sendtoline.pyを実行しました。3回"test"に送信します。\n1回目')
    test.msg_test('2回目')
    test.stk('3回目','high')
