import os
import pickle
import re
import inspect


class EasyFile:
    def __init__(self):
        self.a = 'a'

    def __str__(self):
        ef = EasyFile()
        text = ''
        i = 1
        for x in inspect.getmembers(ef, inspect.ismethod):
            if re.match('__',x[0]) != None:
                continue
            text += x[0]
            if i % 4 == 0:
                text += '()\n'
            else:
                text += '(), '
            i += 1
        del ef
        return text

class EasyTxt:
    def __init__(self,the_file=None):
        self.path = 'C:\\Users\\kizuk\\Desktop\\python\\txt\\'
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


class EasyPickle:
    def __init__(self):
        self.path = 'C:\\Users\\kizuk\\Desktop\\python\\pickle\\'
        self.path_dict = {}
    def __str__(self):
        ep = EasyPickle()
        text = ''
        i = 1
        for x in inspect.getmembers(ep, inspect.ismethod):
            if re.match('__',x[0]) != None:
                continue
            text += x[0]
            if i % 4 == 0:
                text += '()\n'
            else:
                text += '(), '
            i += 1
        del ep
        return text

    def set_path(self,filename):
        if re.search('.pickle',filename) != None:
            filename = re.split('.',filename)[0]
        if not filename in self.path_dict:
            self.path_dict[filename] = self.path + filename + '.pickle'
        path = self.path_dict[filename]
        filename += '.pickle'
        return filename,path
    def save(self,filename,data):
        f,path = self.set_path(filename)
        with open(path,'wb') as file:
            pickle.dump(data,file)
        print('EasyPickle: save: '+f)
    def load(self,filename):
        f,path = self.set_path(filename)
        with open(path,'rb') as file:
            data = pickle.load(file)
        print('EasyPickle: load: '+f)
        return data
