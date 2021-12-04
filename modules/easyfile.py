import os
import sys
import pickle
import re
import inspect
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class EasyJson:
    def __init__(self,filename):
        self._path = 'data/json/{}.json'.format(filename)
        if not os.path.exists(self._path):
            with open(self._path, 'w', encoding="utf-8") as f:
                json.dump('', f, indent=4, ensure_ascii=False)
    def save(self,data):
        with open(self._path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    def load(self):
        with open(self._path,'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

class EasyPickle:
    def __init__(self, filename):
        self._path = 'data/pickle/{}.pickle'.format(filename)
        if not os.path.exists(self._path):
            with open(self._path,'wb') as f:
                pickle.dump('',f)
    def save(self,data):
        with open(self._path, 'wb') as f:
            pickle.dump(data,f)
    def load(self):
        with open(self._path, 'rb') as f:
            data = pickle.load(f)
        return data



class EasyTxt:
    def __init__(self,the_file=None):
        self.path = 'data/'
        self.path_dict = {}
        self.the_file = None

        if the_file != None:
            self.set_path(the_file)
            self.the_file = the_file
    def set_path(self,filename=None):
        if self.the_file != None:
            name = self.the_file
            path = self.path_dict[name]
        else:
            if re.search('.txt',filename) != None:
                filename = re.split('.',filename)[0]
            if not filename in self.path_dict:
                self.path_dict[filename] = self.path + filename + '.txt'
            path = self.path_dict[filename]
            name = filename + '.txt'
        return name,path
    def make_file(self,filename=None):
        name,path = self.set_path(filename)
        with open(path,'x') as file:
            file.write('')
    def add(self,text,filename=None):
        name,path = self.set_path(filename)
        with open(path,'a') as file:
            file.write(text)
    def add_line(self,text,filename=None):
        text_shaped = '\n' + text
        self.add(text_shaped,filename)
