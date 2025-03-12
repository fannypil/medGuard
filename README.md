# **MedGuard**
---

## **Project Overview**
MedGuard is an IoT-driven health monitoring system designed to track patient vitals, including heart rate and body temperature, in real-time. Using MQTT protocol. The system includes multiple sensor-based modules and a graphical monitoring interface, ensuring real-time alerts in case of abnormal readings.
---

## **Features**

✅**Continuous Health Tracking** – Monitors heart rate & temperature via IoT sensors.

✅**Emergency Alert System** – A dedicated button to trigger alerts via MQTT.

✅**User-Friendly Dashboard** – PyQt5-based GUI for real-time monitoring.

✅**Data Logging** – Stores patient data in an SQLite database.

✅**Configurable MQTT Settings** – Easily adjustable broker parameters.

---

## **🔧 System Components**

🔹 **Heart Rate Sensor** (`HBDet.py`)  
   - Measures heart rate and sends data via MQTT, with a graphical PyQt5 interface.

🔹 **Temperature Sensor** (`TDet.py`)  
   - Tracks body temperature and transmits updates to the system.
   - Provides a PyQt5 GUI for real-time temperature monitoring.  

🔹 **Emergency Button** (`BUTTON.py`)  
   - Allows patients to send an immediate distress signal via MQTT when pressed.  
   - Provides a PyQt5 GUI for the emergency button.  

🔹 **Monitoring Dashboard** (`MonitorGUI.py`)  
   - Displays real-time patient data and alerts.  
   - Provides a PyQt5 GUI for monitoring and visualization.  

🔹 **MQTT Client & Data Manager** (`app_manager.py` , `mqtt_init.py`)  
   - Handles MQTT connections and subscriptions.
   - Stores health data in an **SQLite database** (`health_data.db`).  
   - Processes incoming messages and triggers alerts when necessary.

---

## **🚀 Installation Guide

### **Prerequisites**
Ensure the following dependencies are installed:  
- **Python 3.7+**  
- **PyQt5** (`pip install PyQt5`)  
- **Paho-MQTT** (`pip install paho-mqtt`)  
- **SQLite3** (included with Python)  

### **Setup Instructions**

1️⃣ **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd medGuard
    ```

2️⃣ **Set Up a Virtual Environment:**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3️⃣ **Install required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4️⃣ **Run the Manager**:
    ```sh
    python app_manager.py
    ```

5️⃣ **Run the Emergency Button GUI**:
    ```sh
    python BUTTON.py
    ```

6️⃣ **Run the Heart Rate Detector GUI**:
    ```sh
    python HBDet.py
    ```

7️⃣ **Run the Temperature Detector GUI**:
    ```sh
    python TDet.py
    ```

8️⃣ **Open Monitoring Dashboard**:
    ```sh
    python MonitorGUI.py
    ```

💡 **Tip:** Run each component in a **separate terminal window** for smooth operation.

---
## **🖥 System Flow**

1️⃣ **Sensors collect health data** and send readings to the MQTT broker.
2️⃣ The **emergency button**  triggers alerts via MQTT when pressed.  
3️⃣ The **monitoring dashboard** displays real-time data and alerts, updating automatically with new sensor readings.  
4️⃣ The **MQTT client** processes incoming messages and stores health data in the **SQLite database**.  
5️⃣ Alerts are triggered in case of abnormal readings, ensuring timely intervention.

---

## **📊Database Structure (health_data.db)**
- Every MQTT message is recorded in an **SQLite database** (`health_data.db`).  
- Stored data includes **timestamps, topics, and messages** for better tracking and analysis.  
---

## 💡Acknowledgements
- This project was developed as part of an IoT coursework.
- [Paho MQTT](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [IceCream](https://github.com/gruns/icecream)


