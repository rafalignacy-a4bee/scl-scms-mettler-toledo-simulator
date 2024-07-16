from PyQt5.QtCore import QThread, pyqtSignal
import serial
import time
import serial.serialutil

class SerialWorker(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None
        self.port_opened = True

    def run(self):
        self.serial_port = serial.Serial(self.port, self.baudrate)
        
        if self.port_opened:
            message = b'S S      0.000 kg\r\n'
            for _ in range(5):
                try:
                    self.serial_port.write(message)
                except serial.serialutil.PortNotOpenError:
                    pass
                time.sleep(0.1)

        while self.port_opened:
            try:
                if self.serial_port.in_waiting > 0:
                    data = self.serial_port.readline().decode('utf-8').strip()
                    self.data_received.emit(data)
            except:
                if self.serial_port.is_open:
                    self.serial_port.reset_input_buffer()

    def stop(self):
        if self.serial_port.is_open:
            self.serial_port.reset_input_buffer()
            self.serial_port.close()
        self.port_opened = False

    def send_data(self, message):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(message.encode('utf-8'))
            except serial.serialutil.PortNotOpenError:
                print("Serial write error")