import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
import paho.mqtt.client as mqtt
import socket

# Get IP address of the host
socketport     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_connection = socketport.connect(("8.8.8.8", 80))
ipaddress      = socketport.getsockname()[0]
broker_address = ipaddress

# connect with the MQTT Broker
user = "snake"
password = "classic"
port=1883

class SliderWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create four sliders
        self.scale_factor = 100
        #self.scale_factor = 1000
        self.k_p = QSlider()
        self.k_p.setOrientation(Qt.Vertical)
        self.k_p.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.k_p.setMaximum(10000) # Actual value is equal to this divided by self.scale_factor
        self.k_d = QSlider()
        self.k_d.setOrientation(Qt.Vertical)
        self.k_d.setMinimum(1)  # Actual value is equal to this divided by self.scale_factor
        self.k_d.setMaximum(10000) # Actual value is equal to this divided by self.scale_factor
        self.var_a = QSlider()
        self.var_a.setOrientation(Qt.Vertical)
        self.var_a.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.var_a.setMaximum(10000) # Actual value is equal to this divided by self.scale_factor
        self.var_w = QSlider()
        self.var_w.setOrientation(Qt.Vertical)
        self.var_w.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.var_w.setMaximum(10000) # Actual value is equal to this divided by self.scale_factor

        # Create four labels for the sliders
        label1 = QLabel('k_p')
        label2 = QLabel('k_d')
        label3 = QLabel('a')
        label4 = QLabel('w')

        # Create four labels for the slider values
        value_label1 = QLabel()
        value_label2 = QLabel()
        value_label3 = QLabel()
        value_label4 = QLabel()

        # Create a layout for each slider
        layout1 = QVBoxLayout()
        layout1.addWidget(label1)
        layout1.addWidget(self.k_p)
        layout1.addWidget(value_label1)
        layout2 = QVBoxLayout()
        layout2.addWidget(label2)
        layout2.addWidget(self.k_d)
        layout2.addWidget(value_label2)
        layout3 = QVBoxLayout()
        layout3.addWidget(label3)
        layout3.addWidget(self.var_a)
        layout3.addWidget(value_label3)
        layout4 = QVBoxLayout()
        layout4.addWidget(label4)
        layout4.addWidget(self.var_w)
        layout4.addWidget(value_label4)

        # Create a layout for the window and add the slider layouts to it
        hbox = QHBoxLayout()
        hbox.addLayout(layout1)
        hbox.addLayout(layout2)
        hbox.addLayout(layout3)
        hbox.addLayout(layout4)

        # Set the window layout
        self.setLayout(hbox)

        # Set the window size and title
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Snake Robot Parameters')

        # Connect the valueChanged signals of the sliders to update the value labels
        self.k_p.valueChanged.connect(lambda value: self.update_value_label(value_label1, value, 'k_p'))
        self.k_d.valueChanged.connect(lambda value: self.update_value_label(value_label2, value, 'k_d'))
        self.var_a.valueChanged.connect(lambda value: self.update_value_label(value_label3, value, 'a'))
        self.var_w.valueChanged.connect(lambda value: self.update_value_label(value_label4, value, 'w'))

    def update_value_label(self, label, value, title):
        # Update the value label with the slider value
        label.setText(f'Value: {value/self.scale_factor}')

        message = title + ',' + str(value/self.scale_factor)
        # Print the slider value in the terminal
        print(f'Slider value: {message}')


        self.connect_mosquitto('snake_robot_params', message)

    def connect_mosquitto(self, topic, message):
        
        mqtt_client = mqtt.Client()
        mqtt_client.username_pw_set(user, password)
        mqtt_client.connect(broker_address, 1883)
        mqtt_client.publish(topic, str(message))

if __name__ == '__main__':
    # Create the application and window objects
    app = QApplication(sys.argv)
    slider_window = SliderWindow()

    # Show the window and start the event loop
    slider_window.show()
    sys.exit(app.exec_())