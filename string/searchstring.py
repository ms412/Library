import re

class searchstring(object):

    def __init__(self):
        self._str = './'

    def search_numbers(self,str):
        substr = re.search("[-+]?\d+[\.]?\d*", str)
       #      m = re.search("[-+]?\d+[\.]?\d*", line)
      #  print(substr)
       # print(substr.group())

        return substr.group()

