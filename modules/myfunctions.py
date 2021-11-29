from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def find_it(selector):
    try:
        script = "document.querySelector('"+selector+"').scrollIntoView(true)"
        driver.execute_script(script)
        return driver.find_element_by_css_selector(selector)
    except:
        print('"'+selector+'"が見つかりませんでした')
def click_it(selector):
    script = "document.querySelector('"+selector+"').scrollIntoView(true)"
    driver.execute_script(script)
    script = "document.querySelector('"+selector+"').click()"
    driver.execute_script(script)
    #element = driver.find_element_by_css_selector(selector)
    #element.click()
    time.sleep(0.5)
def write_it(selector,text):
    script = "document.querySelector('"+selector+"').scrollIntoView(true)"
    driver.execute_script(script)
    element = driver.find_element_by_css_selector(selector)
    element.clear()
    element.send_keys(text)
def wait_with_id(id):
    wait.until(EC.element_to_be_clickable((By.ID,id)))
def wait_with_selector(selector):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,selector)))
def wait_and_click(selector):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,selector)))
    click_it(selector)
def wait_loading():
    print('wait')
    wait.until(EC.presence_of_element_located((By.ID,'loading-modalOverlay')))
    print('visible')
    wait.until(EC.invisibility_of_element_located((By.ID,'loading-modalOverlay')))
    print('invisible')
