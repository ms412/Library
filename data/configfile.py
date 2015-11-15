
from configobj import ConfigObj
from library.broker.msgbus import msgbus


class configmng(msgbus):

    def __init__(self,OutChannel = None,InChannel = None):

        self.cfghandle = ''

        self.OutChannel = OutChannel

        if (InChannel == None):
            self.msgbus_subscribe(InChannel, self.cfghandle)


    def open(self, filename):
        '''
        opens a config and reads the content
        '''
        self.cfghandle = ConfigObj(filename)
        print(self.cfghandle.keys())
        return self.cfghandle

    def write(self, filename):
        '''
        write configuration to file
        '''
        self.cfghandle.filename = filename
        self.cfghandle.write()
        return True

    def setCfg(self,msg):
        '''
        receives messages from messagebus
        '''
        self.cfghandle= msg
        return True

    def read(self):
        '''
        sends config through messagebus
        '''
        if (self.OutChannel != None):
            self.msgbus_publish(self.OutChannel,self.cfghandle)

        return self.cfghandle.dict()

if __name__ == '__main__':

    cfg = configmng()
    cfg.open('configfile')
    logcfg = cfg.getCfg
    print('Log',logcfg.keys())
    print(logcfg['Loging'])