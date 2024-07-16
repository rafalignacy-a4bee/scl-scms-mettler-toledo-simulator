from PyQt5.QtCore import QThread
import time
import copy

class ComPortsTracker(QThread):
    def __init__(self, com_ports, combobox):
        super().__init__()
        self.com_ports = com_ports
        self.previous_com_ports = copy.deepcopy(com_ports)
        self.combobox = combobox
    
    def run(self):
        while True:
            if sorted(self.previous_com_ports) != sorted(self.com_ports):
                self.combobox.clear()
                self.combobox.addItems(sorted(self.com_ports))
                self.previous_com_ports = copy.deepcopy(self.com_ports)
            time.sleep(0.01)