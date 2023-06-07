import pyvisa
import numpy as np
import time

class Counter_53131A:
    def __init__(self, bus_connection:str = "GPIB0",simulation = True):
        self.name = "Universal Counter 53131A"
        self.bus = bus_connection
        if not self.SIM:
             self.init_visa_connection()
    
    def __name__(self):
        return "indicator"

    def init_visa_connection(self):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus, read_termination = "\r")
        self.inst.timeout = 50000
        return 0
    
    def reset(self):
        self.inst.write("*RST")
        return 0
