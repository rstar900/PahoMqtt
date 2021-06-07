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

    Steps:-

    1. Turn on the broker
    2. Run the subsciber
    3. After the subscriber is started, run the publisher as well

    Info :-  This program quits after receiving the first message from a publisher (basically waits till it receives atleast one message)
'''

import paho.mqtt.client as mqtt

# when 1st message is received print it, disconnect and exit the program
def on_message(client, userdata, message):
    client.message_received = True
    print('Received message')
    print('message:', str(message.payload.decode('UTF-8')))
    print('Disconnecting now')
    client.loop_stop()
    client.disconnect()
    exit(0)

# when subscibtion is successful, acknowledge it 
def on_subscribe(client, userdata, mid, granted_qos):
    print('Subscribed to house/bulb1')
    return

broker = 'BROKER_IP_ADDRESS' # Broker's IP address
port = '' # Broker's port address (not necessary as defaults to 1883)

# creating a class member flag to indicate if a message is received or not
mqtt.Client.message_received = False

# defining the client object and the required callbacks
client = mqtt.Client('Python-Subscriber')
client.on_subscribe = on_subscribe
client.on_message = on_message


# connect and subscribe
try:

    client.connect(broker)
    ret, mid = client.subscribe('house/bulb1', 1)

    if not ret == 0:
        print('Could not subscribe')

    client.loop_start() # start a loop to handle callbacks and connection in another thread

    while client.message_received == False:
        #do nothing and just wait to keep the progran running long enough for the first message to be received
        pass

# if exception occurs
except:
    print('could not connect')
    exit(1)