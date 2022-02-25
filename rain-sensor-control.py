import threading 
from time import sleep 
import paho.mqtt.client as mqtt

# ฟังก์ชันน้ำฝน
def rain():
    while True:
        print('rain')
        if stop_threads:
            break

# set new thread
def setThread():
    global rainrun
    rainrun =  threading.Thread(name ='rain',target=rain)

# เชื่อมต่อ MQTT Host
def on_connect(mqtt_c,userdata,flags,rc):
    global stop_threads
    if rc==0:
        print("Connected OK")
        # เมื่อทำเชื่อมต่อสำเร็จให้รันน้ำฝน
        setThread()
        stop_threads = False
        rainrun.start()
    else:
        print("Bad connetion Retruned Code=",rc)

# รับคำสั่ง MQTT 
def on_message(mqtt_c, userdata, message):
    global stop_threads
    msg = message.payload.decode("utf-8", "strict")
    print(msg) #แสดงข้อความ
    # สั่งเริ่มการทำงานน้ำฝน
    if msg == "start":
        setThread()
        stop_threads = False
        rainrun.start()
    # สั่งหยุดการทำงานน้ำฝน
    elif msg == "stop":
        stop_threads = True
        rainrun.join()

mqtt_c=mqtt.Client('weather') 
mqtt_c.on_connect=on_connect
mqtt_c.on_message = on_message
mqtt_c.connect("127.0.0.1") # mqtt ที่เชื่อมต่อ
mqtt_c.subscribe("TEST") # หัวข้อที่รับ
mqtt_c.loop_forever()