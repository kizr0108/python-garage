import time
import datetime
import re
import sys
import os
from bs4 import BeautifulSoup
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules import sendtoline
from modules import easyselenium
from modules import easyfile

stl = sendtoline.SendToLine()
ep = easyfile.EasyPickle()

########## ログイン ##########
es = easyselenium.EasySelenium(headless=False)
es.get('https://webmail.jikei.ac.jp/',sleeptime=5)
es.write_all([['input[name="twuser"]','h27ms-horimi'],['input[name="twpassword"]','kazuki213322']])
es.click('input[type="submit"]',sleeptime=1)

es.click('input[value="クリア"]',0.4)
for i in range(4):
    es.click('div[style*="/images/imatrix/a1.gif"]',0.4)
es.click('input[value="ログイン"]',8.0)


########## 操作関数定義 ##########
def check_mail_and_notify():
    try:
        time.sleep(10)
        es.click('table#rmail',3.0)
        es.iframe_in('#contentIframe',3.0)
        es.select('#select_filter',value='filter_unseen')

        selector_pre = 'div#divListGrid > table > tbody > tr:nth-of-type(2) > td > div > div > table > tbody > tr'
        tr_num = es.count(selector_pre)
        mail_alluser = []
        mail_not_alluser = 0
        while tr_num != 1:
            #未読メールの内、[Alluser]でないもののメール本文を送信し、[Alluser]のメールはタイトルだけ表示
            for i in range(2,tr_num+1):
                time.sleep(2)
                selector = selector_pre + ':nth-of-type(' + str(i) + ') > td:nth-of-type('
                title = es.text(selector + '6)')
                if re.search(r'Alluser',title) != None:
                    mail_alluser.append(title)
                    es.click(selector + '6)',1.0)
                else:
                    author = es.text(selector + '7)')
                    day = es.text(selector + '8)')
                    es.click(selector + '6)',1.0)
                    content = es.text('#mailviewer_body > tt')

                    content = re.sub(r'brbr',r'\n\n',re.sub(r'\n','',re.sub(r'\n\n+','brbr',content)))
                    sendtext2 = '\n==== @jikei newmail ====\n{}\n--------------------\n送信者:{}\n日時:{}\n--------------------\n{}\n===================='.format(title,author,day,content)
                    stl.send(sendtext2)
                    mail_not_alluser += 1
            time.sleep(1.0)
            es.click('#_mail_action_button_reload')
            tr_num = es.count(selector_pre)

        if mail_alluser != []:
            sendtext1 = '\n==== @jikei newmail ====\n'
            for title in mail_alluser:
                sendtext1 += title + ', '
            sendtext1 = sendtext1[:-2] + '\n=========='
            stl.send(sendtext1)
        if mail_alluser == [] and mail_not_alluser == 0:
            stl.send('新着メッセージ無し')
        es.iframe_out(5.0)
    except:
        text = el.error_info()
        stl.send(text)

def alluser_into_trash():
    es.click('table#rmail',5.0)
    es.iframe_in('#contentIframe',5.0)
    es.write(['input#skeyword','Alluser'])
    es.click('button#rmail_search_button',5.0)

    pagemax = int(es.text('#listPageMax'))
    for i in range(pagemax):
        es.click('#divListGrid input[type="checkbox"]',2.0)
        es.driver.execute_script('mailControl.moveTrash();')
        time.sleep(5)
    es.iframe_out(5.0)

def all_mail_read():
    es.click('table#rmail',5.0)
    es.iframe_in('#contentIframe',5.0)
    es.select('#select_filter',value='filter_unseen')
    #es.select('list_page_size_select',value='100')

    tr_num = 0
    selector_pre = 'div#divListGrid > table > tbody > tr:nth-of-type(2) > td > div > div > table > tbody > tr'
    while tr_num != 1:
        tr_num = es.count(selector_pre)
        print('tr_num:'+str(tr_num))
        es.click('#divListGrid input[type="checkbox"]',2.0)
        es.driver.execute_script('mailControl.setSeen();')
        time.sleep(1.5)
    es.iframe_out(5.0)


##メールリストselector #divListGrid > table > tbody > tr:nth-of-type(2) > td > table tbody tr
##td 6番目 件名 7番目 送信者 8番目 日時

##########関数実行 ##########
#alluser_into_trash()
#all_mail_read()
check_mail_and_notify()


########## 終了 ##########
es.quit()
