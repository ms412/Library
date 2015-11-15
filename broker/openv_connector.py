
import time
import telnetlib
import json

from queue import Queue
from threading import Thread, Lock
from library.broker.msgbus import msgbus

class openv_connector(Thread, msgbus):
    '''
    classdocs
    '''

    def __init__(self,config,msgbus_out,msgbus_log='LOG'):
        Thread.__init__(self)

        self._logChannel = msgbus_log
        self._msgBusOut = msgbus_out

        msg = 'create object'
        self.msgbus_publish(self._logChannel,'%s openv_connector: %s '%('DEBUG',msg))

        self._cfg = config
        self.log_queue = Queue()

        self._host = config.get('HOST','localhost')
        self._port = config.get('PORT',3002)
        self._commands = config.get('COMMANDS')

        self._handle_tn = None
        self._connected = False

    def __del__(self):
        msg = 'delete object'
        self.msgbus_publish(self._logChannel,'%s openv_connector: %s '%('DEBUG',msg))


    def run(self):
     #   print('start openv connector')
        msg = 'start thread'
        self.msgbus_publish(self._logChannel,'%s openv_connector: %s '%('DEBUG',msg))


        #self.setup()
        time.sleep(3)
        threadRun = self.connect()

      # threadRun = True

        while threadRun:

            result = {}

            for command in self._commands:

                temp_list = self.read(command )
                temp_dict = {'VALUE':temp_list[0],'TYPE':temp_list[-1]}
                result.update({command:temp_dict})

            self.msgbus_publish(self._msgBusOut,result)

        return True

    def connect(self):
        result = False
        try:
            self._handle_tn = telnetlib.Telnet('192.168.1.155', 3002,10)
        except:
            msg = 'failed to connect'
            self.msgbus_publish(self._logChannel,'%s openv_connector: %s '%('ERROR',msg))
            result = False
           # print ("Connection ERROR")
        else:
            self._handle_tn.read_until(b"vctrld>", 5)
        #    print('2')
            time.sleep(1)
            msg = 'connect to openv'
            self.msgbus_publish(self._logChannel,'%s openv_connector: %s '%('DEBUG',msg))
            self._connected = True
            print('connected')
            result = True

        return result

    def read(self, command):
            self._handle_tn.write(command.encode('ascii')+ b"\n")
            #   session.write("command".encode('ascii') + b"\r")
            result = self._handle_tn.read_until(b"vctrld>", 5).strip(b"\nvctrld>")
            result = result.decode("utf-8")

            return result
           # liststring1 = result.split(' ',1)