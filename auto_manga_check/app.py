import sys
import os
import time
from bs4 import BeautifulSoup
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config
from modules import easyselenium_ver2_under_update as easyselenium
from modules import easylogger
from modules import sendtoline
from modules.easyfile import EasyPickle

es = easyselenium.EasySelenium(headless=True)
stl = sendtoline.SendToLine()
el = easylogger.EasyLogger('auto_manga_check')
ep = EasyPickle('manga_list')

dict_url = {
    'This is good':'https://manga1001.com/%e3%81%93%e3%81%86%e3%81%84%e3%81%86%e3%81%ae%e3%81%8c%e3%81%84%e3%81%84-raw-free/',
    'Parallel':'https://manga1001.com/%e3%83%91%e3%83%a9%e3%83%ac%e3%83%ab%e3%83%91%e3%83%a9%e3%83%80%e3%82%a4%e3%82%b9-raw-free/',
    'dungeon':'https://manga1001.com/%e3%82%bb%e3%83%83%e3%82%af%e3%82%b9%ef%bc%86%e3%83%80%e3%83%b3%e3%82%b8%e3%83%a7%e3%83%b3-%ef%bd%9e%e6%88%91%e3%81%8c%e5%ae%b6%e3%81%ae%e5%9c%b0%e4%b8%8b%e3%81%abh%e5%9b%9e%e6%95%b0%ef%bc%9d%e3%83%ac%e3%83%99%e3%83%ab%e3%81%ae%e3%83%80%e3%83%b3%e3%82%b8%e3%83%a7%e3%83%b3%e3%81%8c%e5%87%ba%e7%8f%be%e3%81%97%e3%81%9f%ef%bd%9e-raw-free/',
    'dr.stone':'https://manga1001.com/%e3%83%89%e3%82%af%e3%82%bf%e3%83%bc%e3%82%b9%e3%83%88%e3%83%bc%e3%83%b3-dr-stone-raw-free1/',
    'so-so furiiren':'https://manga1001.com/%e8%91%ac%e9%80%81%e3%81%ae%e3%83%95%e3%83%aa%e3%83%bc%e3%83%ac%e3%83%b3-raw-free/',
    'monday':'https://manga1001.com/%e6%9c%88%e6%9b%9c%e6%97%a5%e3%81%ae%e3%81%9f%e3%82%8f%e3%82%8f-raw-free/',
    'recommend children':'https://manga1001.com/%e6%8e%a8%e3%81%97%e3%81%ae%e5%ad%90-raw-free/',
    'heliocentric theory':'https://manga1001.com/%e3%83%81%e3%80%82%e2%88%92%e5%9c%b0%e7%90%83%e3%81%ae%e9%81%8b%e5%8b%95%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6%e2%88%92-raw-free/',
    'guilty':'https://manga1001.com/%e3%82%ae%e3%83%ab%e3%83%86%e3%82%a3%e3%82%b5%e3%83%bc%e3%82%af%e3%83%ab-raw-free/',
    'grand blue':'https://manga1001.com/%e3%81%90%e3%82%89%e3%82%93%e3%81%b6%e3%82%8b-raw-free/',
    'ONE PIECE':'https://manga1001.com/%e3%83%af%e3%83%b3%e3%83%94%e3%83%bc%e3%82%b9-raw-free1/',
    'HUNTER HUNTER':'https://manga1001.com/hunter-x-hunter-raw-free/',
    'HANCHOU':'https://manga1001.com/1%e6%97%a5%e5%a4%96%e5%87%ba%e9%8c%b2%e3%83%8f%e3%83%b3%e3%83%81%e3%83%a7%e3%82%a6-raw-free/',
    'my home hero':'https://manga1001.com/%e3%83%9e%e3%82%a4%e3%83%9b%e3%83%bc%e3%83%a0%e3%83%92%e3%83%bc%e3%83%ad%e3%83%bc-raw-free/',
}
def run():
    selector = '.chaplist tr:first-of-type a'
    line = ''
    dict_latest_contents = ep.load()
    for book,url_root in dict_url.items():
        es.get(url_root)
        try:
            es.ec_wait_selector(selector)
        except:
            html = es.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html,'html.parser')
        html = es.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html,'html.parser')
        a = soup.select_one(selector)
        title, url = a.get_text(), a.get('href')
        if book not in dict_latest_contents or dict_latest_contents[book] != title:
            dict_latest_contents[book] = title
            line += '\n{}:{}'.format(book,url)
    es.quit()
    if line != '':
        stl.send(line)
    else:
        stl.send('新着マンガなし')
    ep.save(dict_latest_contents)
    return line

if __name__ == '__main__':
    run()
