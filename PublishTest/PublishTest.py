#!python3

'''
    code referred from http://www.steves-internet-guide.com/publishing-messages-mqtt-client/

    Another great reference for understanding the network loop, 
    http://www.steves-internet-guide.com/loop-python-mqtt-client/

    need to run mosquitto -c <path to conf file>

    for now, can use 'sudo tail -f /var/log/mosquitto/mosquitto.log' for debugging in another terminal

    or if you just want to see the actual message published on any topic use
    mosquitto_sub -v -t '#' in another terminal

    'listner 1883' and 'allow_anonymous true' fields need to be set in conf file

    Also if your broker is running on a VM, make sure to use bridged network instead of NAT, 
    for the VM to get its own unique public IP on the nework 
'''

import paho.mqtt.client as mqtt

# What to do on a publish event
def on_publish(client, userdata, mid):
    print('Data published\n')
    client.is_published = True
    client.loop_stop()
    return

broker = '192.168.0.111' # Broker's IP address
port = '' # Broker's port address (not necessary as defaults to 1883)

mqtt.Client.is_published =  False

client = mqtt.Client('Python-Client') # Create a mqtt client object
client.on_publish = on_publish # define an on_publish function for the client

# Connect to the broker and attempt to publish (default QoS = 0)
try:
    client.connect(broker)
    ret,mid = client.publish('house/bulb1', 'ON')
    
    client.loop_start()

    if not ret == 0:
        print('Could not publish')
        
    while(client.is_published == False):
        pass

except:
    print('Could not connect to broker')
    exit(1)

client.disconnect()
exit(0) 

