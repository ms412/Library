
import time
#import datetime

from queue import Queue
from threading import Thread, Lock
from library.broker.msgbus import msgbus



class logging(Thread, msgbus):
    '''
    classdocs
    '''

    def __init__(self,config,msgbus_log='LOG'):
        Thread.__init__(self)
        print('init logging')

        self._cfg = config
        self.log_queue = Queue()

        self._logChannel = msgbus_log
        self.msgbus_subscribe(self._logChannel, self._log_sink)

        self._logFile = config.get('LOGFILE', '/var/log/mqtt2gpio.log')

        self.log_ready = False
        self.logHandle = ''
        self._logFileHandle = None
        self._logFileName = None
        self._logLevel = 0


    def run(self):
        print('run logging adapter')

       # self.setup()

        threadRun = True

        while threadRun:
            time.sleep(5)
         #   print('logging loop Mode:', self.log_ready)

         #   while not self.cfg_queue.empty():
          #      self.on_cfg(self.cfg_queue.get())

            if self.log_ready:
                self.openfile()
                while not self.log_queue.empty():
                    # self.on_log(self.log_queue.get())
                    self.filter(self.log_queue.get())
                self.closefile()

        return True

    def _log_sink(self, log_msg):
        print('LOG:',log_msg)
        self.log_queue.put(log_msg)
        return True

  #  def _on_cfg(self, cfg_msg):
        # print('CONFIG LOG',cfg_msg)
   #     self.cfg_queue.put(cfg_msg)
    #    return True

    def filter(self, msg):

        if msg.startswith('INFO'):
            logtype = 1
        elif msg.startswith('WARNING'):
            logtype = 2
        elif msg.startswith('ERROR'):
            logtype = 3
        else:
            logtype = 4

      #  print('LOG filter:',logtype,self._logLevel)

        if logtype >= self._logLevel:
            self.writefile(msg)

        return True


    def on_cfg(self, cfg_msg):
        # print('Config message',cfg_msg)
        general = cfg_msg.select('GENERAL')
        print('LOG CONFIGURATION', general)
        self.msgbus_publish('LOG', '%s Logger Configuration %s ' % ('INFO', general.getTree()))

        self._logFileName = general.getNode('LOGFILE', '/var/log/mqtt2gpio.log')
        logmode = general.getNode('LOGMODE', 'INFO')

        if 'INFO' in general.getNode('LOGMODE', 'INFO'):
            self._logLevel = 1
        elif 'WARNING' in general.getNode('LOGMODE', 'INFO'):
            self._logLevel = 2
        elif 'ERROR' in general.getNode('LOGMODE', 'INFO'):
            self._logLevel = 3
        else:
            self._logLevel = 4

        print('LOG loglevel',self._logLevel)

        self.log_ready = True

        return True

    def openfile(self):
      #  print('LOG: Openlogfile', self._logFileName)
        self._logFileHandle = open(self._logFile, "a")
        return True

    def closefile(self):
     #   print('LOG: Closelogfile', self._logFileHandle)
        self._logFileHandle.closed
        return True

    def writefile(self, logdata):
      #  print('LOG timestamp:',self.timestamp())
        self._logFileHandle.write(str(self.timestamp()) + '\t' + logdata + '\n')
       # self._logFileHandle.write(logstring)
        return True

    def timestamp(self):
      #  return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S').format
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())