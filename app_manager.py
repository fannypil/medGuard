
import paho.mqtt.client as mqtt
import time

import random
from mqtt_init import *

from icecream import ic
from datetime import datetime

import sqlite3


def time_format():
    return f'{datetime.now()}  Manager|> '

ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False) # use True for including script file context file  

# Define callback functions
def on_log(client, userdata, level, buf):
        ic("log: "+buf)
            
def on_connect(client, userdata, flags, rc):    
    if rc==0:
        ic("connected OK")                
    else:
        ic("Bad connection Returned code=",rc)
        
def on_disconnect(client, userdata, flags, rc=0):    
    ic("DisConnected result code "+str(rc))
        
def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    ic("message from: " + topic, m_decode)
    if "Temperature" in m_decode:
            try:
                #Extrect temp value
                temp_value = float(m_decode.split("Body Temperature: ")[1].split("°C")[0])
                save_to_db("Temperature", temp_value)  # Save to DB
                # if temp > 39 send Alert
                if temp_value > temp_TRH_High:
                    alert_message = f"⚠️ High Fever Alert! Detected Body Temperature: {temp_value}°C"
                    ic("Sending High Fever Alert...")
                    send_msg(client, "medGuard/patient/emergency/sts", alert_message)

                # if temp < 35 send Alert
                elif temp_value < temp_TRH_Low:
                    alert_message = f"⚠️ Low Body Temperature Alert! Detected Body Temperature: {temp_value}°C"
                    ic("Sending Low Body Temperature Alert...")
                    send_msg(client, "medGuard/patient/emergency/sts", alert_message)

            except ValueError:
                ic("Error: Could not parse temperature value.")
    if "Heart" in m_decode:
        try:
            heart_rate_value = int(m_decode.split("Heart Rate: ")[1].split("BPM")[0])
            save_to_db("Heart Rate", heart_rate_value)  # Save to DB
            if heart_rate_value > Heart_Rate_TRH_High:
                alert_message = f"⚠️ High Heart Rate Alert! Detected Heart Rate: {heart_rate_value} BPM"
                ic("Sending High Heart Rate Alert...")
                send_msg(client, "medGuard/patient/emergency/sts", alert_message)

            elif heart_rate_value < Heart_Rate_TRH_Low:
                alert_message = f"⚠️ Low Heart Rate Alert! Detected Heart Rate: {heart_rate_value} BPM"
                ic("Sending Low Heart Rate Alert...")
                send_msg(client, "medGuard/patient/emergency/sts", alert_message)

        except ValueError:
            ic("Error: Could not parse heart rate value.")


def send_msg(client, topic, message):
    ic("Sending message: " + message)    
    client.publish(topic, message)   

def client_init(cname):
    r=random.randrange(1,10000000)
    ID=str(cname+str(r+21))
    client = mqtt.Client(ID, clean_session=True) # create new client instance
    # define callback function       
    client.on_connect=on_connect  #bind callback function
    client.on_disconnect=on_disconnect
    client.on_log=on_log
    client.on_message=on_message        
    if username !="":
        client.username_pw_set(username, password)        
    ic("Connecting to broker ",broker_ip)
    client.connect(broker_ip,int(port))     #connect to broker
    return client

def create_database():

    conn = sqlite3.connect("health_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS health_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        metric_type TEXT,
                        value REAL
                    )''')

    conn.commit()
    conn.close()
def save_to_db(metric_type, value):

    conn = sqlite3.connect("health_data.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO health_metrics (metric_type, value) VALUES (?, ?)", (metric_type, value))

    conn.commit()
    conn.close()
def fetch_data():
    conn = sqlite3.connect("health_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_metrics ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    print("📊 *Health Data Log*")
    print("-" * 50)
    for row in rows:
        print(f"ID: {row[0]}, Time: {row[1]}, Type: {row[2]}, Value: {row[3]}")
def main():
    cname = "Manager-"
    client = client_init(cname)
    # main monitoring loop
    client.loop_start()  # Start loop
    client.subscribe('medGuard/patient/5976397/sts')
    try:
        while conn_time==0:           
            time.sleep(conn_time+manag_time)
            ic("Time for sleep: "+str(conn_time+manag_time))
            time.sleep(3)       
        ic("con_time ending") 
    except KeyboardInterrupt:
        client.disconnect() # disconnect from broker
        ic("interrrupted by keyboard")

    client.loop_stop()    #Stop loop
    # end session
    client.disconnect() # disconnect from broker
    ic("End manager run script")

if __name__ == "__main__":
    create_database()
    main()