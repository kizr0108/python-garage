import configparser
import json
from importlib import import_module
import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
INI_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'log.json')

from modules import easylogger

el = easylogger.EasyLogger(rootname='autorun_manager', level='debug')

def get_apps():
    #自動実行するアプリと自動実行するかを取得
    #形式は{appname1:bool,appname2:bool,...}
    el.info('---------- start get_apps() ----------')
    dict = {}
    config_ini = configparser.ConfigParser()
    config_ini.read(INI_PATH, encoding='utf-8')
    list = config_ini['AUTORUN APP LIST']
    el.debug('in [AUTORUN APP LIST]')
    for app in list:
        el.debug('found:{} = {}'.format(app,list[app]))
        if list[app] == 'True':
            bool = True
        else:
            bool = False
        dict[app] = bool
    el.info('---------- end get_apps() ----------')
    return dict

def update_ini(dict):
    el.info('---------- start update_ini() ----------')
    config_ini = configparser.RawConfigParser()

    section = 'AUTORUN APP LIST'
    config_ini.add_section(section)
    for i,j in dict.items():
        config_ini.set(section,i,j)

    with open(INI_PATH, 'w') as file:
        config_ini.write(file)
    el.info('---------- end update_ini() ----------')

def update_apps():
    #全フォルダを走査し、settings.pyから自動実行するアプリを抽出
    #フォルダ名に「.」を含まず、かつapp.py、settings.pyがあるフォルダをアプリと定義する
    #アプリのsettings.pyを参照し、app_for_auto_runがTrueの物を自動実行するアプリとする
    el.info('---------- start add_newapps() ----------')
    apps_autorun = []
    root = './'
    flist = os.listdir(root)
    for f in flist:
        el.debug('found:./'+f)
        if f == 'autorun_manager':
            el.debug('this file/folder is autorun_manager')
            continue
        if '.' in f:
            el.debug('this file/folder has "."')
            continue
        if f == 'app_template':
            el.debug('this file/folder is app_template')
            continue
        if not os.path.isdir(root+f):
            el.debug('this is NOT folder')
            continue
        if not (os.path.exists(root+f+'/app.py') and os.path.exists(root+f+'/settings.py')):
            el.debug('this folder has NOT app.py or settings.py')
            continue
        el.debug('    this is APP')
        settings = import_module(f+'.settings')
        if hasattr(settings, 'APP_FOR_AUTO_RUN'):
            el.debug('    [{}/settings.py]APP_FOR_AUTO_RUN = {}'.format(f,str(settings.APP_FOR_AUTO_RUN)))
            if settings.APP_FOR_AUTO_RUN == True:
                apps_autorun.append(f)

    #config.iniを参照し、新しくアプリが追加されていたら自動実行Trueで書き込み
    #追加されていなければconfig.iniは上書きしない
    appdict = get_apps()
    for app in apps_autorun:
        if app not in appdict:
            appdict[app] = True
            el.debug('add:{} = True'.format(app))
    dellist = []
    for key in appdict.keys():
        if key not in apps_autorun:
            dellist.append(key)
    for item in dellist:
        appdict.pop(item)
        el.debug('delete:{} = True'.format(item))
    update_ini(appdict)
    el.info('---------- end add_newapps() ----------')
    return appdict

def run_all(dict):
    for key,value in dict.items():
        if value == True:
            with open(LOG_PATH,'r') as log_json:
                log_dict = json.load(log_json)
            if key not in log_dict:
                log_dict[key] = []
            el.debug(log_dict)

            app = import_module(key+'.app')
            result_text = app.run()

            time = datetime.now().strftime('%Y/%m/%d %H:%M')
            result = [[time,result_text]]
            el.debug(result)
            result.extend(log_dict[key])
            el.debug(result)
            if len(result) == 6:
                result.pop(5)
            log_dict[key] = result
            el.debug(log_dict)

            with open(LOG_PATH, 'w') as f:
                json.dump(log_dict, f, indent=4, ensure_ascii=False)

def run_it(appname):
    with open(LOG_PATH,'r') as log_json:
        log_dict = json.load(log_json)
    if appname not in log_dict:
        log_dict[appname] = []
    el.debug(log_dict)

    app = import_module(appname+'.app')
    result_text = app.run()

    time = datetime.now().strftime('%Y/%m/%d %H:%M')
    result = [[time,result_text]]
    el.debug(result)
    result.extend(log_dict[appname])
    el.debug(result)
    if len(result) == 6:
        result.pop(5)
    log_dict[appname] = result
    el.debug(log_dict)

    with open(LOG_PATH, 'w') as f:
        json.dump(log_dict, f, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    appdict = update_apps()
    run_all(appdict)
    try:
        a=1
    except:
        warning = el.error_info()
        el.warning('!!!!! ERROR !!!!!')
        el.warning(warning)
