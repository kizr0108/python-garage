from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import inspect
import re
import sys
import os
import platform
from functools import wraps
from bs4 import BeautifulSoup
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from . import easylogger
from . import sendtoline
import config

el = easylogger.EasyLogger('easyselenium','info')
stl = sendtoline.SendToLine()
sleeptime = 5

#################
#デコレータ
#################
def page_transition_limit(func):
    @wraps(func)
    def _limit_wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        time.sleep(.5)
        return val
    return _limit_wrapper

@el.deco_class_info('info')
class EasySelenium:
    def __init__(self,implicitly_wait=5,headless=False):
        run_os = platform.system()
        if run_os == 'Linux': #heroku上で実行している場合
            self._DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
        elif run_os == 'Windows':
            self._DRIVER_PATH = '/Users/kizuk/Desktop/python/auto_run/chromedriver'
        self._options = Options()
        self._options.add_argument('--disable-gpu');
        self._options.add_argument('--disable-extensions');
        self._options.add_argument('--proxy-server="direct://"');
        self._options.add_argument('--proxy-bypass-list=*');
        self._options.add_argument('--start-maximized');
        #セキュリティ対策
        self._ua = UserAgent()
        self._options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1')
        if headless == True or run_os == 'Linux':
            self._options.add_argument('--headless');
        #self._PROFILE_PATH = '/Users/kizuk/AppData/Local/Google/Chrome'
        #self._options.add_argument('--user-data-dir=' + PROFILE_PATH) #ログイン状態保持したい場合
        self.driver = webdriver.Chrome(executable_path=self._DRIVER_PATH, options=self._options)
        self.driver.implicitly_wait(implicitly_wait)
        self._timeout = 10

        #セキュリティ対策
        self._RECAPTCHA_API_KEY = config.RECAPTCHA_API_KEY



    def __str__(self):
        es = EasySelenium(headless=True)
        text = ''
        i = 1
        for x in inspect.getmembers(es, inspect.ismethod):
            if re.match('__',x[0]) != None:
                continue
            text += x[0]
            if i % 4 == 0:
                text += '()\n'
            else:
                text += '(), '
            i += 1
        es.quit()
        del es
        return text


    #################
    #待機処理
    #################
    #非同期通信を行っているサイトでは、wait_allは欲しい情報が来る前に動作停止する為役に立たない
    def ec_wait_all(self):
        WebDriverWait(self.driver,self._timeout).until(EC.presence_of_all_elements_located)
    def ec_wait_selector(self,selector,e=False):
        if not e:
            try:
                WebDriverWait(self.driver, self._timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            except TimeoutException:
                return
                html = self.driver.page_source.encode('utf-8')
                soup = BeautifulSoup(html,'html.parser')
                print(soup)
    def ec_wait_text(self,selector,text):
        try:
            WebDriverWait(self.driver, self._timeout).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector),text))
        except TimeoutException:
            return
            '''
            el.error(el.error_info)
            html = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html,'html.parser')
            print(soup)'''
    def ec_presence_of_element_located(self,selector):
        WebDriverWait(self.driver, self._timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    @page_transition_limit
    def get(self,url):
        self.driver.get(url)
    def quit(self):
        self.driver.quit()

    @page_transition_limit
    def click(self,selector,e=False):
        self.ec_wait_selector(selector,e)
        self._scroll(selector)
        script = "document.querySelector('"+selector+"').click()"
        self.driver.execute_script(script)
    @page_transition_limit
    def click_all(self,selector_list,e=False):
        list = selector_list
        for selector in list:
            self.ec_wait_selector(selector,e)
            self._scroll(selector)
            script = "document.querySelector('"+selector+"').click()"
            self.driver.execute_script(script)
    def write(self,list,e=False):
        #list = [selector,text]
        self.ec_wait_selector(list[0],e)
        self._scroll(list[0])
        element = self.driver.find_element_by_css_selector(list[0])
        element.clear()
        element.send_keys(list[1])
    def write_all(self,list,e=False):
        #list = [[selector,text],...]
        for item in list:
            self.ec_wait_selector(item[0],e)
            self._scroll(item[0])
            element = self.driver.find_element_by_css_selector(item[0])
            element.clear()
            element.send_keys(item[1])
    def find(self,selector,e=False):
        self.ec_wait_selector(selector,e)
        return self.driver.find_element_by_css_selector(selector)
    def text(self,selector,e=False):
        self.ec_wait_selector(selector,e)
        self._scroll(selector)
        element = self.driver.find_element_by_css_selector(selector)
        return element.text
    def select(self,selector,index=None,text=None,value=None,e=False):
        self.ec_wait_selector(selector,e)
        select = Select(self.driver.find_element_by_css_selector(selector))
        if index != None and text == None and value == None:
            select.select_by_index(index)
        if index == None and text != None and value == None:
            select.select_by_visible_text(text)
        if index == None and text == None and value != None:
            select.select_by_value(value)
    def deselect_all(self,selector,e=False):
        self.ec_wait_selector(selector,e)
        select = Select(self.driver.find_element_by_css_selector(selector))
        select.deselect_all()
    def get_attr(self,selector,attrname,e=False):
        #attributeをget
        self.ec_wait_selector(selector,e)
        element = self.driver.find_element_by_css_selector(selector)
        return element.get_attribute(attrname)
    def count(self,selector,e=False):
        self.ec_wait_selector(selector,e)
        elements = self.driver.find_elements_by_css_selector(selector)
        return len(elements)

    @page_transition_limit
    def iframe_in(self,iframe_selector,e=False):
        self.ec_wait_selector(iframe_selector,e)
        iframe = self.driver.find_element_by_css_selector(iframe_selector)
        self.driver.switch_to_frame(iframe)
    def iframe_out(self,e=False):
        self.driver.switch_to.default_content()
    def alert_accept(self):
        alert = self.driver.switch_to_alert()
        alert.accept()
    def alert_dismiss(self):
        alert = self.driver.switch_to_alert()
        alert.dismiss()



    def _scroll(self,selector,e=False):
        self.ec_wait_selector(selector,e)
        script = "document.querySelector('"+selector+"').scrollIntoView(true)"
        self.driver.execute_script(script)

    def recaptcha(self,selector):
        #以下は以前使用したもののコピペ
        #recaptchaのidや送信ボタンのclass等が
        #recaptchaによって違う可能性もあるので
        #ひとまずこの形で保存
        solver = TwoCaptcha(self.RECAPTCHA_API_KEY)
        data_sitekey = es.get_attr('#recaptcha','data-sitekey')
        response = solver.recaptcha(sitekey=data_sitekey, url=es.driver.current_url)
        code = response['code']
        textarea = es.driver.find_element_by_id('g-recaptcha-response')
        es.driver.execute_script(f'arguments[0].value = "{code}";', textarea)
        es.click('span.exportButtonContent')

if __name__ == '__main__':
    a = EasySelenium(headless=True)
    print(a)
    a.quit()



################################################################################
#class SelectorError(Exception):
#    def __init__(self,)
