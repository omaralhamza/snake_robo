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

        # Create 7 sliders
        self.scale_factor = 10000
        #self.scale_factor = 1000
        self.k_p = QSlider()
        self.k_p.setOrientation(Qt.Vertical)
        self.k_p.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.k_p.setMaximum(30000) # Actual value is equal to this divided by self.scale_factor
        self.k_d = QSlider()
        self.k_d.setOrientation(Qt.Vertical)
        self.k_d.setMinimum(1)  # Actual value is equal to this divided by self.scale_factor
        self.k_d.setMaximum(30000) # Actual value is equal to this divided by self.scale_factor
        self.var_a = QSlider()
        self.var_a.setOrientation(Qt.Vertical)
        self.var_a.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.var_a.setMaximum(1500000) # Actual value is equal to this divided by self.scale_factor
        self.var_w = QSlider()
        self.var_w.setOrientation(Qt.Vertical)
        self.var_w.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.var_w.setMaximum(100000) # Actual value is equal to this divided by self.scale_factor
        self.var_d = QSlider()
        self.var_d.setOrientation(Qt.Vertical)
        self.var_d.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.var_d.setMaximum(62800) # Actual value is equal to this divided by self.scale_factor        
        self.var_phi0 = QSlider()
        self.var_phi0.setOrientation(Qt.Vertical)
        self.var_phi0.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.var_phi0.setMaximum(1000000) # Actual value is equal to this divided by self.scale_factor
        self.var_phi1 = QSlider()
        self.var_phi1.setOrientation(Qt.Vertical)
        self.var_phi1.setMinimum(1) # Actual value is equal to this divided by self.scale_factor
        self.var_phi1.setMaximum(1000000) # Actual value is equal to this divided by self.scale_factor
        
        # Create 7 labels for the sliders
        label1 = QLabel('k_p')
        label2 = QLabel('k_d')
        label3 = QLabel('a')
        label4 = QLabel('w')
        label5 = QLabel('d')
        label6 = QLabel('phi0')
        label7 = QLabel('phi1')
    

        # Create 6 labels for the slider values
        value_label1 = QLabel()
        value_label2 = QLabel()
        value_label3 = QLabel()
        value_label4 = QLabel()
        value_label5 = QLabel()
        value_label6 = QLabel()
        value_label7 = QLabel()

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
        layout5 = QVBoxLayout()
        layout5.addWidget(label5)
        layout5.addWidget(self.var_d)
        layout5.addWidget(value_label5)
        layout6 = QVBoxLayout()
        layout6.addWidget(label6)
        layout6.addWidget(self.var_phi0)
        layout6.addWidget(value_label6)
        layout7 = QVBoxLayout()
        layout7.addWidget(label7)
        layout7.addWidget(self.var_phi1)
        layout7.addWidget(value_label7)

        # Create a layout for the window and add the slider layouts to it
        hbox = QHBoxLayout()
        hbox.addLayout(layout1)
        hbox.addLayout(layout2)
        hbox.addLayout(layout3)
        hbox.addLayout(layout4)
        hbox.addLayout(layout5)
        hbox.addLayout(layout6)
        hbox.addLayout(layout7)

        # Set the window layout
        self.setLayout(hbox)

        # Set the window size and title
        self.setGeometry(100, 100, 450, 450)
        self.setWindowTitle('Snake Robot Parameters')

        # Connect the valueChanged signals of the sliders to update the value labels
        self.k_p.valueChanged.connect(lambda value: self.update_value_label(value_label1, value, 'k_p'))
        self.k_d.valueChanged.connect(lambda value: self.update_value_label(value_label2, value, 'k_d'))
        self.var_a.valueChanged.connect(lambda value: self.update_value_label(value_label3, value, 'a'))
        self.var_w.valueChanged.connect(lambda value: self.update_value_label(value_label4, value, 'w'))        
        self.var_d.valueChanged.connect(lambda value: self.update_value_label(value_label5, value, 'd'))
        self.var_phi0.valueChanged.connect(lambda value: self.update_value_label(value_label6, value, 'phi0'))
        self.var_phi1.valueChanged.connect(lambda value: self.update_value_label(value_label7, value, 'phi1'))

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