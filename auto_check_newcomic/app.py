import sys
import os
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules import sendtoline
from modules import easyselenium

stl = sendtoline.SendToLine()
es = easyselenium.EasySelenium(headless=True)

url = 'https://manga1001.com/%e3%81%93%e3%81%86%e3%81%84%e3%81%86%e3%81%ae%e3%81%8c%e3%81%84%e3%81%84-raw-free/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
es.get(url)
html = es.driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
print(soup)

title = soup.find('h1').text
stl.send(title)
