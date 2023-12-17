#!/usr/bin/env python3
import paho.mqtt.client as mqtt #import the client1
import time
import logging as log

from ina219 import INA219
from ina219 import DeviceRangeError

def publish_INA219_value():
    client.publish(INA219_current_name,ina.current()*(-1)/1000)

def on_disconnect(client, userdata, rc=0):
    log.info("Disconnected: result code="+str(rc))
    log.info("Will try to reconnect")
    log.info("connecting to broker")
    client.connect(broker_address) #connect to broker
    log.info("connected to broker") 

###################################
# logging setup
#log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/var/log/mqtt_clients/INA219.log', filemode='w', level=log.INFO)
log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/var/log/mqtt_clients/INA219.log', level=log.INFO)

#SHUNT_OHMS = 0.0001
#ina = INA219(SHUNT_OHMS)
ina = INA219(shunt_ohms=0.0001,
             max_expected_amps = 400,
             address=0x40)

ina = INA219(shunt_ohms=0.0001,
             max_expected_amps = 400,
             address=0x40)

ina.configure(voltage_range=ina.RANGE_16V,
              gain=ina.GAIN_1_40MV,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

# mqtt topic names for BME280
INA219_current_name = "/myhome/INA219/current"

# mqtt client connection
broker_address="nassynology.ddns.net"
#broker_address="localhost"
print("creating new instance")
client = mqtt.Client("INA219") #create new instance
client.username_pw_set(username="pi",password="slademla")
client.on_disconnect = on_disconnect
print("connecting to broker")
client.connect(broker_address) #connect to broker
print("succesfully connected to the broker")
t=3
while True:
    try:
        publish_INA219_value()
        #print("%.3f mA" % ina.current())
        time.sleep(t)
    except Exception as e:
        log.error('Exception: %s \nWill try to restart the client.', e)
        client.connect(broker_address)
