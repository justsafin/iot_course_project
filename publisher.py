import random
import paho.mqtt.client as mqtt
import time
import numpy as np
import matplotlib.pyplot as plt

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
client.username_pw_set("kamilkamil", "WarHammer40k")

# connect to HiveMQ Cloud on port 8883
client.connect("6d975d04bb24486d98151dbccc67c39f.s1.eu.hivemq.cloud", 8883)

i = 400
i_list = []
for x in range(-3000,3000,250):
    y = -0.57 * ((x/1000) ** 2) + 21
    i_list.append(y)

# plt.plot(np.arange(-6, 6, 0.5), i_list, label='Temperature', color='r')
# plt.show()

def get_temp(i, i_list = i_list):
    i = i//100
    s = np.random.normal(i_list[i], 0.5, 1)
    temperature =  s[0]
    return temperature

graph_wide = 100

temp_visible = np.zeros(graph_wide)
x_axis = np.arange(graph_wide)

while True:
    if i%100 ==0:
        temperature = get_temp(i)
    data = "{0},{1}".format(i, temperature)
    print(data)

    new_visible = np.delete(temp_visible, 0)
    temp_visible = np.append(new_visible, temperature)

    plt.cla()
    plt.title('График температуры')
    plt.plot(x_axis, temp_visible, label='Temperature', color='r')
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    plt.ylim(14,25)
    plt.pause(0.05)

    client.loop_start()
    client.publish("my/test/topic1", data)
    client.loop_stop()
    i+= 50
    # time.sleep(1)
    if i == 2400:
        i = 0


