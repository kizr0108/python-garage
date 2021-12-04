from logging import getLogger,StreamHandler,FileHandler,Formatter,handlers,DEBUG,INFO,WARNING,ERROR
import sys
import re
import os
import traceback
from functools import wraps
import inspect
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

'''
# https://qiita.com/shotakaha/items/0fa2db1dc8253c83e2bb
# ↑ログファイルのローテーティングはまだ理解していないため
#困ったら上をよむこと
'''

class EasyLogger:
    _dict_level = {'debug':DEBUG,'info':INFO,'warning':WARNING,'error':ERROR}
    def __init__(self,rootname,level='warning'):
        root_folder = 'data/log/{}/'.format(rootname)
        if not os.path.exists(root_folder):
            os.mkdir(root_folder)

        self._logger = getLogger(rootname)
        formatter = Formatter('%(asctime)s: %(levelname)s: %(message)s')
        self._sh = StreamHandler()
        #self._fh = FileHandler(filename=r'.\data\log\{}\{}.log'.format(rootname,rootname), encoding='utf-8')
        self._fh = handlers.RotatingFileHandler(filename=r'.\data\log\{}\{}.log'.format(rootname,rootname),maxBytes=100000,backupCount=3, encoding='utf-8')
        self._sh.setFormatter(formatter)
        self._fh.setFormatter(formatter)
        self._logger.addHandler(self._sh)
        self._logger.addHandler(self._fh)

        self._sh.setLevel(EasyLogger._dict_level[level])
        self._fh.setLevel(EasyLogger._dict_level[level])
        self._logger.setLevel(EasyLogger._dict_level[level])

    def debug(self,text):
        self._logger.debug(text)
    def info(self,text):
        self._logger.info(text)
    def warning(self,text):
        self._logger.warning(text)
    def error(self,text):
        self._logger.error(text)
    def _echo_log_dependent_on_level(self,text,level):
        self.debug(text) if level == 'debug' else self.info(text) if level == 'info' else self.warning(text) if level == 'warning' else self.error(text)

    def set_level(self,level):
        self._sh.setLevel(EasyLogger._dict_level[level])
        self._fh.setLevel(EasyLogger._dict_level[level])
        self._logger.setLevel(EasyLogger._dict_level[level])
    def error_info(self):
        error_fulltext = traceback.format_exc()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        exc_type_name = re.split("'",str(exc_type))[1]
        file_path = exc_tb.tb_frame.f_code.co_filename
        file_name = os.path.split(file_path)[1]
        folder_name = os.path.split(os.path.split(file_path)[0])[1]
        lineno = exc_tb.tb_lineno
        text = '{}: {} [{}][line:{}]\n\n{}'.format(exc_type_name,exc_obj,folder_name+'/'+file_name,lineno,error_fulltext)
        return text

    #関数実行前後にlogを書き込む
    def deco_func_info(self,level):
        def _wrapper(func):
            @wraps(func)
            def _decoration_func(*args, **kwargs):
                try:
                    self._echo_log_dependent_on_level('---------- 関数.{} 実行 ----------'.format(func.__name__),level)
                    echo = lambda filename, line, func: self._echo_log_dependent_on_level(filename,line,func),level)
                    frameinfo = inspect.stack()
                    for i in range(2 if len(frameinfo)> 2 else len(frameinfo)):
                        stack = frameinfo[-i-1]
                        self.info(stack.filename)
                        echo(stack.filename, stack.lineno, stack.function)
                    return func(*args, **kwargs)
                except Exception as e:
                    text = self.error_info()
                    self.error(text)
                    raise e
            return _decoration_func
        return _wrapper

    #クラス内のメソッド全体にdeco_func_infoを仕込む
    #excludeに仕込みたくない関数名をつけることで除外できる
    def deco_class_info(self, level, exclude=[]):
        def _wrapper_class(Cls):
            @wraps(Cls)
            def _decoration_class(*args, **kwargs):
                for name, func in inspect.getmembers(Cls):
                    self.debug('関数{}'.format(name))
                    if name.startswith('__'):
                        if name == '__init__':
                            setattr(Cls, name, self._decorate_init(Cls, level)(func))
                            continue
                        else:
                            continue
                    if callable(getattr(Cls, name)) and not name in exclude:
                        setattr(Cls, name, self.deco_func_info(level)(func))
                return Cls(*args, **kwargs)
            return _decoration_class
        return _wrapper_class
    def _decorate_init(self, Cls, level):
        def _wrapper(init):
            @wraps(init)
            def _decoration(*args, **kwargs):
                filename = inspect.stack()[-1].filename
                self.warning('##################################################')
                self.warning('# クラス.{} 実行. 呼び出し元:{} #'.format(Cls.__name__, re.split(r'\\',filename)[-2]+'/'+re.split(r'\\',filename)[-1]))
                self.warning('##################################################')
                return init(*args, **kwargs)
            return _decoration
        return _wrapper





if __name__ == "__main__":
    level = 'debug'
    el = EasyLogger('easylogger',level)
    el.debug('---------- EasyLogger level:{} ----------'.format(level))
    el.debug('debug')
    el.info('info')
    el.warning('warning')
    el.error('error')
    el.debug('日本語の確認')
