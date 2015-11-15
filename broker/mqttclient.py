__author__ = 'oper'


import time
import os

import paho.mqtt.client as mqtt
from threading import Thread, Lock

from queue import Queue
from library.broker.msgbus import msgbus


class mqttclient(msgbus):

    def __init__(self,config,msgbus_in,msgbus_out,msgbus_log='LOG'):
        Thread.__init__(self)

        self._logChannel = msgbus_log
        self._msgBusOut = msgbus_out

        msg = 'create object'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))
        '''
        setup mqtt broker
        config = dictionary with configuration
        '''

        #self._config = config

        self._host = str(config.get('HOST','localhost'))
        self._port = int(config.get('PORT',1883))
        self._user = str(config.get('USER',None))
        self._passwd = str(config.get('PASSWORD',None))
        self._publish = str(config.get('PUBLISH',None))

        temp_subscribe = config.get('SUBSCRIBE',None)
      #  print('subtemp',temp_subscribe)
        if type(temp_subscribe) is list:
       #     print('LIST')
            items = temp_subscribe
        elif type(temp_subscribe) is str:
        #    print('String')
            items = temp_subscribe.split(",")
        #sub_list = sub_temp.split(",")
        #print('Subscribe',items)
        self._subscribe = []
        for item in items:
         #   print(item)
            if item:
                item += '/'
                item += '#'
                self._subscribe.append(item)

        print('TEMP',self._subscribe)

        '''
        broker object
        '''
        self._mqtt = ''

        '''
        Transmit and Receive Queues objects
        '''
        self._rxQueue = Queue()

       # print('MQTT: Init Mqtt object Startup', self)
        msg = 'Create Object'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))
        '''
        create mqtt session
        '''
        #self.create()
        self._mqttc = mqtt.Client(str(os.getpid()),clean_session=True)

#        self.setup(self._config)
       # self.start()

    def __del__(self):
        msg = 'delete object'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))

      #  print("Delete libmqttbroker")
        self._mqttc.disconnect()

    def start(self):
      #  print('MQTT::start')
        '''
        start broker
        '''
       # self._mqttc=self.create()
        msg = 'start thread'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('INFO',msg))

        self.callback()
      #  print('mqtt', self._host, self._port)
        time.sleep(2)
        self.connect(self._host,self._port)
        time.sleep(5)
        for item in self._subscribe:
         #   print('subscribe:',item)
            self.subscribe(item)
        #self.subscribe('/TEST/#')
          #  time.sleep(5)
        return True

    def restart(self,config):
        msg = 'restart thread'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('INFO',msg))

      #  print('MQTT::restart')
        time.sleep(1)
        for item in self._subscribe:
            self.unsubscribe(item)
        self.disconnect()
       # self.setup(config)
        #time.sleep(1)
        self.reinitialise()
        time.sleep(1)
        self.start()
        return True

    def callback(self):
        '''
        setup callbacks
        '''
     #   print('register callbacks')
        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe
        self._mqttc.on_disconnect = self.on_disconnect
        self._mqttc.on_log = self.on_log
        return True

    def tx_data(self,message):
        msg = 'Messages transmit'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('INFO',msg))

        self.publish(message)
        return True

    def rx_data(self):
        if not self._rxQueue.empty():
            msg = self._rxQueue.get()
         #   message = msg.get('MESSAGE',None)
          #  channel = msg.get('CHANNEL',None)
        else:
            msg = None
           # channel = None

        return msg

    def on_connect(self, client, userdata, flags, rc):
        print('MQTT:: connect to host:', self._host,client,userdata,flags,str(rc))
        msg = 'Connect to Mqtt broker'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))
        self._connectState = True
    #    self.msgbus_publish('LOG','%s Broker: Connected %s'%('INFO', self._connectState))
        return True

    def on_disconnect(self, client, userdata, rc):
        msg = 'Disconnect from Mqtt broker'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))
      #  print('Mqtt:: Disconnect' +str(client)+' '+str(userdata)+' '+str(rc))
        return True

    def on_message(self, client, userdata, msg):
        message ={}
        message.update({'CHANNEL':msg.topic})
        message.update({'MESSAGE':msg.payload})
       # print('MQTT:: on_message:',userdata,msg,message)
        log_msg = 'Message received'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s Channel: %s Message: %s'%('DEBUG',log_msg, msg.topic, msg.payload))
      #  self.msgbus_publish('LOG','%s Broker: received Date Device: %s , Port: %s , Message: %s'%('INFO',message['CHANNEL'], message['PORT_NAME'], message['MESSAGE']))
        self._rxQueue.put(message)
        return True

    def on_publish(self, client, userdata, mid):
        msg = 'Message published'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))
   #     print('MQTT on_published '+str(client)+' '+str(userdata)+' '+str(mid))
        return True

    def on_subscribe(self, client, userdata, mid, granted_qos):
        msg = 'Subscribed to Channel'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))
    #    print('MQTT: on_subscribe: '+str(client)+' '+str(userdata)+' '+str(mid)+' '+str(granted_qos))
        return True

    def on_unsubscribe(self, client, userdata, mid):
        msg = 'Unsubscribe from Channel'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))
     #   print('MQTT:: unsubscribe',client, userdata,mid)
        return True

    def on_log(self, client, userdata, level, buf):
        '''
        Test
        :param client:
        :param userdata:
        :param level:
        :param buf:
        :return:
        '''
      #  print('MQTT: Log',client, userdata, level, buf)
        return True

   # def create(self):
    #    print('mqtt create mqtt object')
     #   return mqtt.Client(str(os.getpid()))

    def reinitialise(self):
        msg = 'Reinitialise'
        self.msgbus_publish(self._logChannel,'%s mqtt client: %s '%('DEBUG',msg))
      #  print('mqtt reinitialise')
        self._mqttc.reinitialise(str(os.getpid()), clean_session=True)
        return True

    def connect(self,host,port):
        #print('COnnect')
        print(host,port)
        self._mqttc.connect(host, port,60)
        #self._mqttc.connect('192.168.1.107', 1883,60)
        self._mqttc.loop_start()
        return True

    def disconnect(self):
       # print('dissconnect')
        self._mqttc.disconnect()
        #self._mqttc.loop_stop()
        #self._mqttc.loop_forever()
        return True

    def subscribe(self,channel = None):
        print('mqtt subscribe',channel)
        self._mqttc.subscribe(channel,0)
        return True

    def unsubscribe(self,channel):
       # print('mqtt unsubscribe')
        self._mqttc.unsubscribe(self._subscribe)
        return True

    def publish(self,message):
        self._mqttc.publish(message.get('CHANNEL'), message.get('MESSAGE'), 0)
        return True

if __name__ == "__main__":

    config1 = {'HOST':'192.168.1.107','PUBLISH':'/TEST','SUBSCRIBE':'/TEST/','CONFIG':'/TEST2/'}
    config2 = {'HOST':'localhost','PUBLISH':'/TEST','SUBSCRIBE':['/TEST1/#','/TEST3','/TEST4']}
    msg = {'CHANNEL':'/TEST/CONFIG','MESSAGE':'{ioioookko}'}
    broker = mqttbroker(config1)
  #  broker = setup(config)
 #   broker.start()

#    broker.connect()
 #   broker.subscribe()
    time.sleep(10)
    broker.restart(config1)
 #   time.sleep(10)

    while True:
        time.sleep(1)
        #broker.publish(msg)
   # time.sleep(2)
