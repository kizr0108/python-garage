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

class EasySelenium:
    def __init__(self,implicitly_wait=1.0,sleep_time=1.0,headless=False):
        self._DRIVER_PATH = '/Users/kizuk/Desktop/python/auto_run/chromedriver'
        self._options = Options()
        self._options.add_argument('--disable-gpu');
        self._options.add_argument('--disable-extensions');
        self._options.add_argument('--proxy-server="direct://"');
        self._options.add_argument('--proxy-bypass-list=*');
        self._options.add_argument('--start-maximized');
        if headless == True:
            self._options.add_argument('--headless');
        #self._PROFILE_PATH = '/Users/kizuk/AppData/Local/Google/Chrome'
        #self._options.add_argument('--user-data-dir=' + PROFILE_PATH) #ログイン状態保持したい場合
        self.driver = webdriver.Chrome(executable_path=self._DRIVER_PATH, options=self._options)
        self.driver.implicitly_wait(implicitly_wait)
        self.sleep_time = sleep_time

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

    def get(self,url,sleeptime=2):
        self.driver.get(url)
        time.sleep(sleeptime)
    def quit(self):
        self.driver.quit()
        sys.exit()
    def ec_wait_all(self,timeout=30):
         WebDriverWait(self.driver,timeout).until(EC.presence_of_all_elements_located)

    def click(self,selector,sleeptime=0.4):
        if sleeptime == None:
            sleeptime = self.sleep_time
        self._scroll(selector)
        script = "document.querySelector('"+selector+"').click()"
        self.driver.execute_script(script)
        time.sleep(sleeptime)
    def click_all(self,selector_list,sleeptime=0.4):
        list = selector_list
        if sleeptime == None:
            sleeptime = self.sleep_time
        for selector in list:
            self._scroll(selector)
            script = "document.querySelector('"+selector+"').click()"
            self.driver.execute_script(script)
            time.sleep(sleeptime)
    def write(self,list,sleeptime=0.4):
        #list = [selector,text]
        self._scroll(list[0])
        element = self.driver.find_element_by_css_selector(list[0])
        element.clear()
        element.send_keys(list[1])
        time.sleep(sleeptime)
    def write_all(self,list,sleeptime=0.4):
        #list = [[selector,text],...]
        for item in list:
            self._scroll(item[0])
            element = self.driver.find_element_by_css_selector(item[0])
            element.clear()
            element.send_keys(item[1])
            time.sleep(sleeptime)
    def find(self,selector):
        return self.driver.find_element_by_css_selector(selector)
    def text(self,selector):
        self._scroll(selector)
        element = self.driver.find_element_by_css_selector(selector)
        return element.text
    def select(self,selector,index=None,text=None,value=None,sleeptime=0.4):
        select = Select(self.driver.find_element_by_css_selector(selector))
        if index != None and text == None and value == None:
            select.select_by_index(index)
        if index == None and text != None and value == None:
            select.select_by_visible_text(text)
        if index == None and text == None and value != None:
            select.select_by_value(value)
        time.sleep(sleeptime)
    def deselect_all(self,selector):
        select = Select(self.driver.find_element_by_css_selector(selector))
        select.deselect_all()
    def get_attr(self,selector,attrname):
        #attributeをget
        element = self.driver.find_element_by_css_selector(selector)
        return element.get_attribute(attrname)
    def count(self,selector):
        elements = self.driver.find_elements_by_css_selector(selector)
        return len(elements)

    def iframe_in(self,iframe_selector,sleeptime=0.4):
        iframe = self.driver.find_element_by_css_selector(iframe_selector)
        self.driver.switch_to_frame(iframe)
        time.sleep(sleeptime)
    def iframe_out(self,sleeptime=0.4):
        self.driver.switch_to.default_content()
        time.sleep(sleeptime)
    def alert_accept(self):
        time.sleep(1)
        alert = self.driver.switch_to_alert()
        alert.accept()
        time.sleep(1)
    def alert_dismiss(self):
        time.sleep(1)
        alert = self.driver.switch_to_alert()
        alert.dismiss()
        time.sleep(1)



    def _scroll(self,selector):
        script = "document.querySelector('"+selector+"').scrollIntoView(true)"
        self.driver.execute_script(script)



if __name__ == '__main__':
    a = EasySelenium(headless=True)
    print(a)
    a.quit()



################################################################################
#class SelectorError(Exception):
#    def __init__(self,)
