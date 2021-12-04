import configparser
from importlib import import_module
import sys
import os
import re
import platform
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
INI_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')

from modules import easylogger
from modules.easyfile import EasyJson
from modules import sendtoline

el = easylogger.EasyLogger(rootname='autorun_manager', level='info')
ej = EasyJson('autorun_manager_log')
stl = sendtoline.SendToLine()

@el.deco_func_info('info')
def get_autorun_app_list():
    #自動実行するアプリと自動実行するかを取得
    #形式は{appname1:[bool,int],appname2:[bool,int],...}
    el.info('---------- start get_autorun_app_list() ----------')
    dict = {}
    config_ini = configparser.ConfigParser()
    config_ini.read(INI_PATH, encoding='utf-8')
    dict_raw = config_ini['AUTORUN APP LIST']
    el.debug('in [AUTORUN APP LIST]')
    for app in dict_raw:
        el.debug('found:{} = {}'.format(app,dict_raw[app]))
        list = re.split(',',dict_raw[app])
        if list[0] == 'True':
            list[0] = True
        else:
            list[0] = False
        list[1] = int(list[1])
        dict[app] = list
    el.info('---------- end get_autorun_app_list() ----------')
    return dict

@el.deco_func_info('info')
def change_autorun_app_status(app_name,app_status,run_frequency):
    el.info('---------- start change_autorun_app_status("{}","{}") ----------'.format(app_name,app_status))
    try:
        dict = get_autorun_app_list
        if app_name not in dict:
            log_status,description = 'ERROR','[ERROR]アプリ名が自動実行リストに存在しません'
            el.debug('[ERROR]アプリ名が自動実行リストに存在しません')
        elif type(app_status) != type(True):
            log_status,description = 'ERROR','[ERROR]要求されたアプリステータスがbool型ではありません'
            el.debug('[ERROR]要求されたアプリステータスがbool型ではありません')
        else:
            dict[app_name] = [app_status,run_frequency]
            el.debug('configparser開始')
            config_ini = configparser.RawConfigParser()
            section = 'AUTORUN APP LIST'
            config_ini.add_section(section)
            for i,j in dict.items():
                config_ini.set(section,i,str(j[0])+','+str(j[1]))
            el.debug('config.ini上書き')
            with open(INI_PATH, 'w', encoding='utf-8') as file:
                config_ini.write(file)
            status,description = 'SUCCESS','[自動実行リストを更新]{}:自動実行 {}'.format(app_name,app_status)
    except:
        text = el.error_info()
        el.error(text)
        status,description = 'ERROR','[ERROR]'+text
    el.info('---------- end change_autorun_app_status() ----------')
    return status,description

@el.deco_func_info('info')
def check_all_apps_status():
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
        if hasattr(settings, 'APP_FOR_AUTO_RUN') and hasattr(settings, 'RUN_FREQUENCY'):
            el.info('    [{}/settings.py]APP_FOR_AUTO_RUN = {}, RUN_FREQUENCY = {}'.format(f,str(settings.APP_FOR_AUTO_RUN),str(settings.RUN_FREQUENCY)))
            if settings.APP_FOR_AUTO_RUN == True:
                apps_autorun.append([f,str(settings.RUN_FREQUENCY)])

    #config.iniを参照し、新しくアプリが追加されていたら自動実行Trueで書き込み
    #追加されていなければconfig.iniは上書きしない
    appdict = get_autorun_app_list()
    for app in apps_autorun:
        if app[0] not in appdict:
            appdict[app[0]] = [True,app[1]]
            el.info('add:{} = True,{}'.format(app,str(settings.RUN_FREQUENCY)))
    dellist = []
    for key in appdict.keys():
        add_dellist = True
        for app in apps_autorun:
            if key == app[0]: add_dellist = False
        if add_dellist: dellist.append(key)
    for item in dellist:
        appdict.pop(item)
        el.info('delete:{}'.format(item))

    config_ini = configparser.RawConfigParser()
    section = 'AUTORUN APP LIST'
    config_ini.add_section(section)
    for i,j in appdict.items():
        config_ini.set(section,i,str(j[0])+','+str(j[1]))
    with open(INI_PATH, 'w', encoding='utf-8') as file:
        config_ini.write(file)

    el.info('---------- end add_newapps() ----------')
    return appdict

@el.deco_func_info('info')
def get_log_autorun():
    log_json = ej.load()
    log_autorun = []
    for key,value in log_json.items():
        if len(value) > 0:
            log_autorun.append([key,value[0]])
    return log_autorun

@el.deco_func_info('info')
def run_all_apps(dict,mode='heroku'):
    log_dict = ej.load()
    try:
        for key,value in dict.items():
            if mode == 'debug' and platform.system() == 'Windows':
                run_app(key)
            if value[0] == True:
                app_log = [] if not key in log_dict else log_dict[key]
                log_size = len(app_log)
                ran_num_today = 0
                for i in range(log_size - 1):
                    str_log_time = app_log[i][0]
                    obj_log_time = datetime.strptime(str_log_time,'%Y/%m/%d %H:%M')
                    if obj_log_time.date() == datetime.now().date():
                        ran_num_today += 1
                if int(value[1]) > ran_num_today:
                    run_app(key)
    except:
        el.error(el.error_info())

@el.deco_func_info('info')
def run_app(appname):
    log_dict = ej.load()
    if appname not in log_dict:
        log_dict[appname] = []
    el.debug(log_dict)

    app = import_module(appname+'.app')
    el.info('実行：{}.py'.format(appname))
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

    ej.save(log_dict)

@el.deco_func_info('info')
def pop_one_item_autorun_log_(appname):
    log_dict = ej.load()
    if appname not in log_dict:
        return
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

    ej.save(log_dict)

@el.deco_func_info('info')
def pop_all_autorun_log():
    log_dict = ej.load()
    el.debug(log_dict)

    new_dict = {}
    for appname in log_dict.keys():
        new_dict[appname] = []

    ej.save(new_dict)
    el.info('autorun_manager_logを空にしました。')


if __name__ == "__main__":
    try:
        #pop_all_autorun_log()
        app_dict = check_all_apps_status()
        run_all_apps(app_dict,mode='debug')
    except:
        warning = el.error_info()
        el.warning('!!!!! ERROR !!!!!')
        el.warning(warning)
