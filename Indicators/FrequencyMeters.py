import pyvisa
from .constants import *

class Counter_53131A:
    def __init__(self, bus_connection:str = 'GPIB0::0::INSTR'):
        self.name = "Universal Counter 53131A"
        self.bus = bus_connection
        self.init_visa_connection()
    
    def __name__(self):
        return "indicator"

    def init_visa_connection(self, termination_character = "\r"):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus, read_termination = termination_character)
        self.inst.timeout = 5000
        return 0
    
    def reset(self):
        self.inst.write("*RST")
        return 0
    
    def disconnect(self):
        self.inst.close()

    def get_IDN(self):
        return self.inst.query("*IDN?")
    
    def get_ERROR(self):
        return self.inst.query(":SYST:ERR?")
    
    def write(self,cmd:str):
        self.inst.write(cmd)

    def set_LPF(self,enable = True):
        if enable == True:
            self.write(":INP1:FILT ON")
        else:
            self.write(":INP1:FILT OFF")
    
    def set_Level(self,nivel_tension):
        if nivel_tension >= -5.125 or nivel_tension <= 5.125:
            self.write(f":SENS:EVEN1:LEV:ABS {nivel_tension}")

    def set_SLOPE(self,polaridad):
        self.write(f":SENS:EVEN1:SLOP {polaridad}")

    def set_SENSTVTY(self,sensibilidad = "MED"):
        if sensibilidad == "HI" :
            self.write(f":SENS:EVEN1:HYST:REL 0")
        elif sensibilidad == "MED" :
            self.write(f":SENS:EVEN1:HYST:REL 50")
        elif sensibilidad == "LO" :
            self.write(f":SENS:EVEN1:HYST:REL 100")

    def set_COUPLING(self,tipo_AC_DC = "AC"):
            self.write(f":INP1:COUP {tipo_AC_DC}")

    def set_IMPEDANCE(self,valor = "1 MOHM"):
            if valor == '50 OHM':
               self.write(":INP1:IMP 50") 
            elif valor == '1 MOHM':
                self.write(":INP1:IMP 1E6") 
    
    def set_Gate_Time(self,time = 5.000):
        self.write(f":FREQ:ARM:STOP:TIM {time}")

    def read(self):
        return self.inst.query("READ?")
        
    def RUN(self):
        self.write(":INIT:CONT ON")
