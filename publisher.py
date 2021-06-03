import random
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

# create the client
client = mqtt.Client()
client.on_connect = on_connect

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("kamilkamil", "There_is_pa55w0rd")

# connect to HiveMQ Cloud on port 8883
client.connect("6d975d04bb24486d98151dbccc67c39f.s1.eu.hivemq.cloud", 8883)

i = 400

def get_temp(i):
    temperature = round(random.uniform(23, 25), 2)
    if i < 700 or i > 2000:
        temperature = temperature - round(random.uniform(2,9),2)
        # print("There cold, temperature is {0}".format(temperature))
    print('now is {0}, temperature is {1}'.format(i, temperature))
    return temperature

temp_value = 1
while temp_value == 1:
    temperature = get_temp(i)
    data = "{0},{1}".format(i, temperature)
    client.loop_start()
    client.publish("my/test/topic1", data)
    client.loop_stop()
    i+= 50
    time.sleep(1)
    if i == 2400:
        i = 0



