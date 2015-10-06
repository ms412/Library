import os

class directory(object):

    def __init__(self):
        self._filepath = './'

    def setpath(self, path):
        self._filepath = path

        return True

    def getfile(self):
        _filelist = []
        for file in os.listdir(self._filepath):
            _filelist.append(file)

        return _filelist

    def getfile_ext_filter(self, filter):
        _filelist = []
        for file in self.getfile():
            if file.endswith(filter):
                _filelist.append(file)

        return _filelist