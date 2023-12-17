#!/bin/sh

nohup /usr/local/bin/mqtt_client_ADSVoltage.py > /var/log/mqtt_clients/mqtt_clients.log 2>&1 &
nohup /usr/local/bin/mqtt_client_BME280.py > /var/log/mqtt_clients/mqtt_clients.log 2>&1 &
nohup /usr/local/bin/mqtt_client_INA219.py > /var/log/mqtt_clients/mqtt_clients.log 2>&1 &
