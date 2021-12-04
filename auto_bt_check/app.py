import time
import re
import math
import random
import sys
import os
import platform
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import config
from modules import  easyselenium_ver2_under_update as easyselenium
from modules import easylogger
from modules import sendtoline as stl

el = easylogger.EasyLogger('auto_bt_check')
if platform.system() == 'Linux':
    sendline = stl.SendToLine() #'health_check'
elif platform.system() == 'Windows':
    sendline = stl.SendToLine('test')
sendtome = stl.SendToLine('test')

user_dict = {}
user_config = config.BT_USER
for user in user_config.split('/'):
    i = user.split(',')
    user_dict[i[0]]=[i[1],i[2],float(i[3])]

URL = 'https://el4.jikei.ac.jp/login/index.php'
css_id, css_pass = 'input#username','input#password'





def true_list(list):
    hour, minute = 14, 30
    delta_time = random.randint(-10,10)
    echotime = str(hour)+'時'+str(minute+delta_time)+'分'

    bool = False
    while bool == False:
        delta_temp = random.normalvariate(0,0.15)
        temp = round(list[2]+delta_temp, 1)
        if temp < 37:
            bool = True
    temp = str(temp) + '℃'
    return [list[0],list[1],echotime,temp]

def health_check(name,true_list):
    es = easyselenium.EasySelenium(headless=False)
    es.get(URL)
    es.write_all([['input#username',true_list[0]],['input#password',true_list[1]]])
    es.click('#loginbtn')
    es.click('a[href="https://el4.jikei.ac.jp/course/view.php?id=1789"]')

    icon = es.get_attr('li.modtype_feedback span.autocompletion > img.icon','title') ##########3/3変更
    match = re.match(r'完了', icon)

    if match == None:
        es.click_all(['li.modtype_feedback div.activityinstance a','a.btn-default'])
        INPUT_NUM = [3,4,5,8,10,11,12]
        for i in range(7):
            selector_pre = 'form#feedback_complete_form > div:nth-of-type('+str(INPUT_NUM[i])+') > div.col-md-9'
            if i < 2:
                selector = selector_pre + ' > input[type="text"]'
                es.write([selector,true_list[2+i]])
            else:
                if i == 3 or i == 4:
                    radionum = 1
                else:
                    radionum = 2
                selector = selector_pre + ' > label:nth-of-type('+str(radionum)+') > input'
                es.click(selector)
            i += 1
        es.click_all(['input#id_savevalues','button[type="submit"]'])

        #戻ってチェックがついたか確認 3/3変更
        es.get('https://el4.jikei.ac.jp/course/view.php?id=1789')
        icon = es.get_attr('li.modtype_feedback span.autocompletion > img.icon','title')
        match = re.match(r'完了', icon)

        if match != None:
            status = [1,'{} {}'.format(name,true_list[3])]
        else:
            status = [2,name]
    else:
        status = [0,name]

    #ログアウト
    es.click_all(['a#dropdown-1','a[aria-labelledby="actionmenuaction-6"]'])
    es.quit()
    return status


##########
def run():
    sendline.send('健康チェック開始')
    try:
        result = ['','','']
        for name,value in user_dict.items():
            list = true_list(value)
            status = health_check(name,list)
            result[status[0]] += '「' + status[1] + '」'
        for i in range(3):
            if result[i] == '':
                result[i] = 'なし'
        text = '\n既に入力済み：{}\n入力完了：{}\nエラー：{}'.format(result[0],result[1],result[2])
        sendline.send(text)
    except:
        text = el.error_info()
        sendline.send(text)
        es.quit()
    return text

if __name__ == "__main__":
    run()
