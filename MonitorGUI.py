import os
import sys
import PyQt5
import random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
import time
import datetime
from mqtt_init import *

# Creating Client name - should be unique
global clientname, CONNECTED, heart_rate
CONNECTED = False
r = random.randrange(1, 100000)
clientname = "IOT_client-Id-" + str(r)
sub_topic = 'medGuard/patient/5976397/sts'
sub_topic_emr = 'medGuard/patient/emergency/sts'


class Mqtt_client():

    def __init__(self):
        # broker IP adress:
        self.broker = ''
        self.topic = ''
        self.port = ''
        self.clientname = ''
        self.username = ''
        self.password = ''
        self.subscribeTopic = ''
        self.publishTopic = ''
        self.publishMessage = ''
        self.on_connected_to_form = ''

    # Setters and getters
    def set_on_connected_to_form(self, on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form

    def get_broker(self):
        return self.broker

    def set_broker(self, value):
        self.broker = value

    def get_port(self):
        return self.port

    def set_port(self, value):
        self.port = value

    def get_clientName(self):
        return self.clientName

    def set_clientName(self, value):
        self.clientName = value

    def get_username(self):
        return self.username

    def set_username(self, value):
        self.username = value

    def get_password(self):
        return self.password

    def set_password(self, value):
        self.password = value

    def get_subscribeTopic(self):
        return self.subscribeTopic

    def set_subscribeTopic(self, value):
        self.subscribeTopic = value

    def get_publishTopic(self):
        return self.publishTopic

    def set_publishTopic(self, value):
        self.publishTopic = value

    def get_publishMessage(self):
        return self.publishMessage

    def set_publishMessage(self, value):
        self.publishMessage = value

    def on_log(self, client, userdata, level, buf):
        print("log: " + buf)

    def on_connect(self, client, userdata, flags, rc):
        global CONNECTED
        if rc == 0:
            # print("connected OK")
            print("GUI connected successfully to MQTT Broker!")
            CONNECTED = True
            self.on_connected_to_form();
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print("DisConnected result code " + str(rc))
        CONNECTED = False

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print("message from:" + topic, m_decode)
        if "Emergency" in m_decode:
            mainwin.EmegancyDock.update_mess_win(m_decode)
        if 'Alert' in m_decode:
            mainwin.EmegancyDock.update_mess_win(m_decode)
        if topic == 'medGuard/patient/5976397/sts':
           mainwin.PatientDataDock.update_mess_win(m_decode)


    def connect_to(self):
        # Init paho mqtt client class
        self.client = mqtt.Client(self.clientname, clean_session=True)  # create new client instance
        self.client.on_connect = self.on_connect  # bind call back function
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)
        # print("Connecting to broker ",self.broker)
        print(f"🔵 Connecting to MQTT Broker at {self.broker}:{self.port}")
        self.client.connect(self.broker, self.port)  # connect to broker

    def disconnect_from(self):
        self.client.disconnect()

    def start_listening(self):
        self.client.loop_start()

    def stop_listening(self):
        self.client.loop_stop()

    def subscribe_to(self, topic):
        if hasattr(self, 'client'):
            if CONNECTED:
                self.client.subscribe(topic)
                print(f"Subscribed to topic: {topic}")
            else:
                print("Can't subscribe. Connection should be established first")
        else:
            print("Error: MQTT client is not initialized. Call connect_to() first.")

    def publish_to(self, topic, message):
        self.client.publish(topic, message)


class MyPatientDock(QDockWidget):
    """Main """

    def __init__(self, mc):
        QDockWidget.__init__(self)
        self.mc = mc
        self.eHostInput = QLineEdit()
        self.eHostInput.setText('5976397')
        formLayot = QFormLayout()
        formLayot.addRow("Patient ID", self.eHostInput)
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("My Patient")

class EmergancyAlertDock(QDockWidget):
    """Publisher """

    def __init__(self, mc):
        QDockWidget.__init__(self)
        self.mc = mc

        self.ePublisherTopic = QTextEdit()
        self.ePublisherTopic.setReadOnly(True)

        formLayot = QFormLayout()
        formLayot.addRow(self.ePublisherTopic)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Notification")
        self.setMinimumSize(300, 250)  # שינוי גודל מינימלי

    # create function that update text in received message window
    def update_mess_win(self, text):
        self.ePublisherTopic.append(text)

class PatientDataDock(QDockWidget):
    """Subscribe """
    def __init__(self, mc):
        QDockWidget.__init__(self)
        self.mc = mc
        self.eSubscribeTopic = QLineEdit()
        self.eSubscribeTopic.setText(sub_topic)

        self.eRecMess = QTextEdit()
        self.eRecMess.setReadOnly(True)

        formLayout = QFormLayout()
        formLayout.addRow("Subscribed Topic:", self.eSubscribeTopic)
        formLayout.addRow("Vitals:", self.eRecMess)


        widget = QWidget(self)
        widget.setLayout(formLayout)
        self.setWidget(widget)
        self.setWindowTitle("Patient Data")

        self.setMinimumSize(300, 250)  # שינוי גודל מינימלי

    def update_mess_win(self, text):
        self.eRecMess.append(text)
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Init of Mqtt_client class
        self.mc = Mqtt_client()

        self.mc.set_broker(broker_ip)
        self.mc.set_port(int(broker_port))
        self.mc.set_clientName(clientname)
        self.mc.set_username(username)
        self.mc.set_password(password)
        print("🔵 Connecting to MQTT broker automatically...")
        self.mc.connect_to()
        self.mc.start_listening()

        self.mc.set_on_connected_to_form(self.on_connected)

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        #self.setGeometry(30, 100, 900, 700)
        self.setGeometry(30, 100, 900, 600)  # גודל חלון מוגדל

        self.setWindowTitle('MedGuard')

        # Init QDockWidget objects
        self.PatientDock = MyPatientDock(self.mc)
        self.EmegancyDock = EmergancyAlertDock(self.mc)
        self.PatientDataDock = PatientDataDock(self.mc)

        self.addDockWidget(Qt.TopDockWidgetArea, self.PatientDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.EmegancyDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.PatientDataDock)

        self.resizeDocks([self.PatientDataDock, self.EmegancyDock], [1, 1], Qt.Horizontal)


    def on_connected(self):
        self.mc.subscribe_to(sub_topic)  # sensor topic
        print(f"✅ Subscribed to topic: {sub_topic}")  # success

        self.mc.subscribe_to(sub_topic_emr)  #emergancy button topic
        print(f"✅ Subscribed to topic: {sub_topic_emr}")  #success

app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
