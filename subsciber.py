import tkinter as tk
import time
from PIL import Image, ImageTk
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "my/test/topic1":
        temp = (msg.payload.decode("utf-8"))
        temp_list = temp.split(',')
        global i_value, time_value, temperature_value
        temp_i = int(temp_list[0])
        temperature_value = float(temp_list[1])
        print("taked data: time is {0} and temperature is {1}".format(temp_i, temperature_value))
        i_value = temp_i/100
        time_value = "{0}:{1}".format((round(i_value // 1)), round((i_value % 1) * 60))


# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("kamilkamil", "There_is_pa55w0rd")

# connect to HiveMQ Cloud on port 8883
client.connect("6d975d04bb24486d98151dbccc67c39f.s1.eu.hivemq.cloud", 8883)

# subscribe to the topic "my/test/topic"
client.subscribe("my/test/topic1")
client.subscribe("my/test/topic_temperature")

current_time = 0
i_value = 0
time_value = 0
temperature_value = 0
cold_flag = 0
temp12 = 20


root = tk.Tk()

canvas = tk.Canvas(root,width=500,height=300)
pilImage = Image.open("rassada_day.png")
image = ImageTk.PhotoImage(pilImage)
canvas.create_image(200, 150, image=image)
time_text = canvas.create_text(400,150, text = "Время {0}".format(current_time))
temperature_text = canvas.create_text(400,180, text = "Температура %.4s"%temperature_value)
grelka_text = canvas.create_text(400,220, text = "Обогреватель")
grelka_indicator = canvas.create_oval(450, 212, 465, 227, width =2)
canvas.pack()


while True:
    client.loop_start()
    client.on_message = on_message
    time.sleep(1)
    client.loop_stop()
    print("time is {0}".format(time_value))
    if current_time != i_value:
        current_time = i_value
        canvas.delete(time_text, temperature_text)
        time_text = canvas.create_text(400, 150, text="Время {0}".format(current_time))
        temperature_text = canvas.create_text(400, 180, text="Температура %.4s" % temperature_value)
        canvas.update()
        canvas.pack()
        if i_value < 7 or i_value > 20:
            print('мало солнца')
            canvas.delete(pilImage)
            pilImage = Image.open("rassada_night.png")
            image = ImageTk.PhotoImage(pilImage)
            imagesprite = canvas.create_image(200, 150, image=image)
            canvas.update()
            canvas.pack()
        elif i_value >= 7 or i_value <= 20:
            print('солнце')
            canvas.delete(pilImage)
            pilImage = Image.open("rassada_day.png")
            image = ImageTk.PhotoImage(pilImage)
            imagesprite = canvas.create_image(200, 150, image=image)
            canvas.update()
            canvas.pack()
        if temperature_value< 18:
            canvas.delete(grelka_indicator)
            grelka_indicator = canvas.create_oval(450, 212, 465, 227, width=2, fill='green')
            canvas.update()
            canvas.pack()
        else:
            canvas.delete(grelka_indicator)
            grelka_indicator = canvas.create_oval(450, 212, 465, 227, width=2)
            canvas.update()
            canvas.pack()
    canvas.update()


root.mainloop()












