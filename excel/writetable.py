
import xlwt

class writeXls(object):
    def __init__(self, data):

        self.data = data
        self.sumWb = xlwt.Workbook()
      #  self.format = workbook.add_format({'bold': True, 'font_color': 'red'})
        self.sheet = None
       # self.sheet = self.sumWb.add_sheet('Sheet1', cell_overwrite_ok=True)

    def createSheet(self,name='Sheet1'):
        self.sheet = self.sumWb.add_sheet(name,cell_overwrite_ok=True)
        return True

    def createTable(self):
        row = 0
        col = 0
        for key, value in self.data.items():
            row = row +1
            col = 0
            for index,data in value.items():

                self.createIndex(col,index)
                self.sheet.write(row,col,data)
                col = col + 1

    def createIndex(self,col,index):
        print('index',col,index)
        self.sheet.write(0,col,index)
        return True

    def writeFile(self,filename):
        self.sumWb.save(filename)