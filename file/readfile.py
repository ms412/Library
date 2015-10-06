
class readfile(object):

    def __init__(self):
        self._filename = 'foo.txt'
        self._filepath = './'
        self._filehandle = None

    def open(self, path, filename):
        if not path:
            path = self._filepath

        if not filename:
            filename = self._filename

       # print('TEST',path +'/' + filename)

        self._filehandle = open(path + '/' + filename)

        return True

    def countlines(self):

        return sum(1 for line in self._filehandle)

    def getline(self,number):
        self._filehandle.seek(0)
        lines = self._filehandle.readlines()
        return lines[number]

    def getline_startwith(self,start_str):
        _linelist = []
        self._filehandle.seek(0)
        lines = self._filehandle.readlines()
        for line in lines:
            if line.startswith(start_str):
                _linelist.append(line)

        return _linelist
