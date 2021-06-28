#!python3

'''
    code referred from http://www.steves-internet-guide.com/client-connections-python-mqtt/

    Another great reference for understanding the network loop, 
    http://www.steves-internet-guide.com/loop-python-mqtt-client/

    need to run mosquitto -c <path to conf file>

    for now, can use 'sudo tail -f /var/log/mosquitto/mosquitto.log' for debugging in another terminal

    'listner 1883' and 'allow_anonymous true' fields need to be set in conf file

    Also if your broker is running on a VM, make sure to use bridged network instead of NAT, 
    for the VM to get its own unique public IP on the nework 
'''

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):

    #rc is the return code
    if rc == 0 :
        print("Successfully connected!")
        client.is_connected = True

    else:
        print("Error connecting:",rc)


broker = '192.168.0.111'
port = '' #not necessary as it is default to 1883, if different then change it and pass it to connect() function

# set the is_connected flag as a variable in Client class
mqtt.Client.is_connected = False

client = mqtt.Client("PythonTest") #create Paho client object
client.on_connect = on_connect #bind the on_connect function as the callback for client object

try:
    client.connect(broker) #connect to broker
    print('Connecting to broker', broker)

    client.loop_start() #start network loop

    while client.is_connected == False: #Wait loop
        print('In wait loop')
        time.sleep(1)

    print('In main loop')

    client.loop_stop() #stop network loop
    client.disconnect() #disconnect from broker

except:
    print('Connection refused!')
    exit(1)







