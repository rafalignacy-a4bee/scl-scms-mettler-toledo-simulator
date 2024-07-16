import sys
from weight import Weight
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
import serial.tools.list_ports

class MainWindow(QMainWindow):
    def __init__(self, com_ports):
        super().__init__()

        self.setWindowTitle("SCL & SCMS Simulator")
        self.setFixedSize(360, 520)

        weight1 = Weight("Weight 1", com_ports)
        weight2 = Weight("Weight 2", com_ports)
        weight3 = Weight("Weight 3", com_ports)
        weight4 = Weight("Weight 4", com_ports)
        weight5 = Weight("Weight 5", com_ports)
        weight6 = Weight("Weight 6", com_ports)

        self.grid_layout = QGridLayout()

        self.grid_layout.addWidget(weight1, 0, 0)
        self.grid_layout.addWidget(weight2, 0, 1)
        self.grid_layout.addWidget(weight3, 1, 0)
        self.grid_layout.addWidget(weight4, 1, 1)
        self.grid_layout.addWidget(weight5, 2, 0)
        self.grid_layout.addWidget(weight6, 2, 1)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_widget.setLayout(self.grid_layout)

app = QApplication(sys.argv)

ports = [port.device for port in serial.tools.list_ports.comports()]
ports.insert(0, "")

window = MainWindow(ports)
window.show()

app.exec()
