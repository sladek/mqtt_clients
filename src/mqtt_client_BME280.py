#!/usr/bin/env python3
import paho.mqtt.client as mqtt #import the client1
import smbus2
import bme280
import time
import logging as log
from Adafruit_BME280 import *

def publish_BME280_values():
    #data =  bme280.sample(bus, address, calibration_params)
    sensor =  BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()
    
    client.publish(BME280_temperature_name,degrees)
    client.publish(BME280_pressure_name,hectopascals)
    client.publish(BME280_humidity_name,humidity)

def on_disconnect(client, userdata, rc=0):
    log.info("Disconnected: result code="+str(rc))
    log.info("Will try to reconnect")
    log.info("connecting to broker")
    client.connect(broker_address) #connect to broker
    log.info("connected to broker") 

########################################
# logging setup
#log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/var/log/mqtt_clients/BME280.log', filemode='w', level=log.INFO)
log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='/var/log/mqtt_clients/BME280.log', level=log.INFO)

refresh_in_sec = 10

# parameters for BME280 senzor
port = 1
address = 0x76
bus = smbus2.SMBus(port)
#calibration_params = bme280.load_calibration_params(bus, address)

# mqtt topic names for BME280
BME280_temperature_name = "/myhome/BME280/temperature"
BME280_pressure_name = "/myhome/BME280/pressure"
BME280_humidity_name = "/myhome/BME280/humidity"

# mqtt client connection
broker_address="nassynology.ddns.net"
#broker_address="localhost"
log.info("creating new instance")
client = mqtt.Client("BME280") #create new instance
client.username_pw_set(username="pi",password="slademla")
client.on_disconnect = on_disconnect
log.info("connecting to broker")
client.connect(broker_address) #connect to broker
log.info("connected to broker") 

# main loop
while True:
    try:
        publish_BME280_values()
        time.sleep(refresh_in_sec)
        # log.info('Published: BME280')
    except Exception as e:
        log.error('Exception: %s \nWill try to restart the client.', e)
        client.connect(broker_address)
