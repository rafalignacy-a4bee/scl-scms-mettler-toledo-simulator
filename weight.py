from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QComboBox, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QSlider
from serial_worker import SerialWorker
from com_ports_tracker import ComPortsTracker

class Weight(QGroupBox):
    def __init__(self, title, com_ports=[]):
        super().__init__(title=title)

        self.connected = False
        self.current_weight_value = 0
        self.tare_weight_value = 0
        self.baudrate = 9600

        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()

        self.com_port_label = QLabel("COM port")
        self.com_port_combobox = QComboBox()
        self.com_port_combobox.addItems(sorted(com_ports))

        self.hbox1.addWidget(self.com_port_label)
        self.hbox1.addWidget(self.com_port_combobox)

        self.current_weight_label = QLabel("Weight value")
        self.current_weight_value_label = QLabel("---")
        self.hbox2.addWidget(self.current_weight_label)
        self.hbox2.addWidget(self.current_weight_value_label)

        self.weight_slider = QSlider(Qt.Horizontal)
        self.weight_slider.setRange(0, 3000)
        self.weight_slider.valueChanged.connect(self.weight_value_change)
        self.weight_slider.setEnabled(False)

        self.tare_label = QLabel("Tare value")
        self.tare_value_label = QLabel("---")
        self.hbox3.addWidget(self.tare_label)
        self.hbox3.addWidget(self.tare_value_label)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(lambda: self.connect_button_clicked(com_ports))

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addWidget(self.weight_slider)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addWidget(self.connect_button)

        self.setLayout(self.vbox)

        self.com_ports_tracker = ComPortsTracker(com_ports, self.com_port_combobox)
        self.com_ports_tracker.start()

    def weight_value_change(self):
        self.current_weight_value = self.weight_slider.value() / 1000
        self.current_weight_value_label.setText(f"{self.current_weight_value:.3f} kg")

    def connect_button_clicked(self, com_ports):
        self.current_weight_value = 0
        self.tare_weight_value = 0
        
        if not self.connected and self.com_port_combobox.currentText():
            self.com_ports_tracker.terminate()
            self.device = self.com_port_combobox.currentText()
            com_ports.remove(self.device)

            self.serial_thread = SerialWorker(self.device, self.baudrate)
            self.serial_thread.data_received.connect(self.serial_port_request)
            self.serial_thread.start()

            self.weight_value_change()
            self.weight_slider.setEnabled(True)
            self.com_port_combobox.setEnabled(False)
            self.connect_button.setText("Disconnect")
            self.connected = True

        elif self.connected:
            self.com_ports_tracker.start()
            com_ports.append(self.device)

            self.serial_thread.stop()

            self.com_port_combobox.setCurrentIndex(0)
            self.weight_slider.setValue(0)
            self.current_weight_value_label.setText("---")
            self.tare_value_label.setText("---")
            self.weight_slider.setEnabled(False)
            self.com_port_combobox.setEnabled(True)
            self.connect_button.setText("Connect")
            self.connected = False

    def serial_port_request(self, request_content):
            response = ""

            if request_content == "T":
                self.tare_weight_value = self.current_weight_value
                self.weight_slider.setValue(0)
                self.tare_value_label.setText(f"{self.tare_weight_value:.3f} kg")
                response = f"T S      {self.tare_weight_value:.3f} kg\r\n"
            elif request_content == "TAC":
                self.current_weight_value = self.tare_weight_value
                self.tare_weight_value = 0
                self.weight_slider.setValue(int(self.current_weight_value * 1000))
                self.tare_value_label.setText("---")
                response = f"S S      {self.tare_weight_value:.3f} kg\r\n"   
            else:
                response = f"S S      {self.current_weight_value:.3f} kg\r\n"

            if self.serial_thread:
                self.serial_thread.send_data(response)