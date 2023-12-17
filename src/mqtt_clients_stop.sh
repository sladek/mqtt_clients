#!/bin/sh

pkill -fx "python3 /usr/local/bin/mqtt_client_ADSVoltage.py"
pkill -fx "python3 /usr/local/bin/mqtt_client_BME280.py"
pkill -fx "python3 /usr/local/bin/mqtt_client_INA219.py"