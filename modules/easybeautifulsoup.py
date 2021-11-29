import requests
from bs4 import BeautifulSoup
import re

url = 'https://docs.google.com/forms/d/e/1FAIpQLSdWhPXwwcaGRU2bKENB7m-roy_Mm7ZdPhDIfbyKvEcMFXL9eA/viewform'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
response.close()

scripts = [n for n in soup.select('body > script')]
script = str(scripts[0])
print(script)
print('=========================')
erasefirst = lambda str: re.sub(r'^[^\[]+\[','[',str)
eraselast = lambda str: re.sub(r'\][^\]]+$',']',str)
eraseouter = lambda str: re.sub(r'^[^\[]+\[','',re.sub(r'\][^\]]+$','',str))
def do(func,val,i=1):
    for num in range(i):
        val = func(val)
    return val
take3 = do(eraseouter,script,3)
print(take3)
print('=========================')
els = r'[^\[\]]*'
pre = r'\[[^\[\]]*'
pro = r'[^\[\]]*\]'
freewrite = pre + pre + pre + pro + pro + pro
choice = r'('+pre + pre + pre + r'(\[('+els+pre+pro+els+r')+\])' + pro + pro + pro+r')'


set = re.findall(choice,take3)
for i in range(len(set)):
    print(str(i)+':'+str(set[i][0]))
set = re.findall(freewrite,take3)
for i in range(len(set)):
    print(str(i)+'freewrite:'+set[i])
