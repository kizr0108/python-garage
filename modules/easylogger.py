from logging import getLogger,StreamHandler,FileHandler,Formatter,DEBUG,INFO,WARNING,ERROR
import sys
import re
import os

class EasyLogger:
    _dict_level = {'debug':DEBUG,'info':INFO,'warning':WARNING,'error':ERROR}
    def __init__(self,rootname,level='warning'):
        self._logger = getLogger(rootname)
        formatter = Formatter('%(asctime)s: %(levelname)s: %(message)s')
        self._sh = StreamHandler()
        self._fh = FileHandler(r'.\log\{}.log'.format(rootname))
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

    def set_level(self,level):
        self._sh.setLevel(EasyLogger._dict_level[level])
        self._fh.setLevel(EasyLogger._dict_level[level])
        self._logger.setLevel(EasyLogger._dict_level[level])
    def error_info(self):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        exc_type_name = re.split("'",str(exc_type))[1]
        file_path = exc_tb.tb_frame.f_code.co_filename
        file_name = os.path.split(file_path)[1]
        lineno = exc_tb.tb_lineno
        text = '{}: {} [{}][line:{}]'.format(exc_type_name,exc_obj,file_name,lineno)
        return text
