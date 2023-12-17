#!/usr/bin/env python3

import paho.mqtt.client as mqtt #import the client1
import os
import glob
import time
import base64
import Adafruit_ADS1x15             # Import the ADS1x15 module.
import logging as log

def publish_ADS_Voltage():
    AD_val()
    client.publish(ads0_topic_name,values[0])
    client.publish(ads1_topic_name,values[1])
    client.publish(ads2_topic_name,values[2])
    client.publish(ads3_topic_name,values[3])

def AD_val():
    #Val_CH = [0]*4
    for i in range(4):
    # Read all the ADC channel values in a list.
    # Read the specified ADC channel using the previously set gain value.
        values[i] = (round(float(adc.read_adc(i, gains[i])) * 0.000125 * correction[i], 2))
        if values[i] < 0.5:
            values[i] = 0.0

def on_disconnect(client, userdata, rc=0):
    log.info("Disconnected: result code="+str(rc))
    log.info("Will try to reconnect")
    log.info("connecting to broker")
    client.connect(broker_address) #connect to broker
    log.info("connected to broker") 

########################################
# logging setup
#log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/var/log/mqtt_clients/ADSVoltage.log', filemode='w', level=log.INFO)
log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/var/log/mqtt_clients/ADSVoltage.log', level=log.WARNING)

refresh_in_sec = 10.0

temp_c=0.0
temp_f=0.0

gains = [1.0, 1.0, 1.0, 1.0]
values = [0.0, 0.0, 0.0, 0.0]
correction = [102.8, 104.4, 115.5371, 115.5371]


adc = Adafruit_ADS1x15.ADS1115()    # Create an ADS1115 ADC (16-bit) instance.

ads0_topic_name = "/myhome/ADSVoltage/0"
ads1_topic_name = "/myhome/ADSVoltage/1"
ads2_topic_name = "/myhome/ADSVoltage/2"
ads3_topic_name = "/myhome/ADSVoltage/3"

broker_address="nassynology.ddns.net"
#broker_address="localhost"
log.info("creating new instance")
client = mqtt.Client("ADS") #create new instance
client.username_pw_set(username="pi",password="slademla")
client.on_disconnect=on_disconnect
log.info("connecting to broker")
client.connect(broker_address) #connect to broker
log.info("successfully connected to broker")
while True:
    try:
        log.info('Publishing ADS voltages')
        publish_ADS_Voltage()
        log.info('Sleeping for refresh_in_sec')
        time.sleep(refresh_in_sec)
    except Exception as e:
        log.error('Exception: %s \nWill try to restart the client.', e)
        client.connect(broker_address)
