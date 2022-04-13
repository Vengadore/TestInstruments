from os import lseek
import pyvisa
import numpy as np
import time
import re
# A device in the 5XXX scheme is meant to generate a value with an associated magnitude.
# We can imitate the behavior of a calibrator by knowing which commands it recieves and
# returning the expected value.

class Fluke_5720A:
    def __init__(self, bus_connection:str = "GPIB0",simulation = True):
        self.name = "FLUKE 5720A"
        self.bus = bus_connection
        self.SN = 829848492
        self.FWrev = "1.01b"
        self.status = False # True = OPERATE <> False = STBY
        self.Magnitudes = ["V","A","DB","DBM","OHM"]
        self.x = "0"
        self.unit = "V"
        self.frequency = "0"
        self.log = False
        self.__name__ = "generator"
        self.SIM = simulation
        if not self.SIM:
            self.init_visa_connection()

    def __str__(self) -> str:
        return f"{self.name}:{self.bus}, {self.x} {self.unit}, {self.frequency} HZ"

    def set_output(self,cmd):
        self.x = cmd.split(" ")[1]
        self.unit = cmd.split(" ")[2]
        # Mandar el comando por visa
        if not self.SIM:
            self.send_visa_cmd(f"OUT {self.x} {self.unit}")

    def set_frequency(self,cmd):
        self.frequency = cmd.split(" ")[0]
        # Mandar el comando por visa
        if not self.SIM:
            self.send_visa_cmd(f"OUT {self.frequency} HZ")

    def init_visa_connection(self):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus)
        return 1

    def send_visa_cmd(self,cmd):
        self.inst.write(cmd)
        self.inst.write("*WAI")
        return 1

    def __call__(self, cmd:str) -> str:
        # Capitalize the whole string
        cmd = cmd.upper()

        # General variables
        input_regular_exp = {}  ## Variable to store regular expressions
        self.messages = []            ## Message to generate
        
        
        ###############################################################################################################
        ### BLOCK 1: regular expressions ##### {Regular expression:(Description, method/function that executes it)} ###
        ###############################################################################################################
        # Search in the command the setting for the output  (REG 1)
        input_regular_exp["(OUT [0-9]{1,4} (" + "|".join([i for i in self.Magnitudes]) + "))"] = ("Sets the output of the instrument",
                                                                                                    self.set_output)
        # Search in the command the frequency               (REG 2)
        input_regular_exp["([0-9]{1,5} HZ)"] = ("Sets the frequency at the output",
                                                self.set_frequency)
        # Search in the commands the IDN                    (REG 3)
        input_regular_exp["(\*IDN\?)"] = ("Asks for the ID of the instrument",
                                          lambda attr:self.messages.append(f"IDN:{self.name},SN:{self.SN},FWrev:{self.FWrev}"))
        # Searcn in the commands the OPERATE                (REG 4)
        input_regular_exp["(OPERATE)"] = ("Operates the instrument",
                                          lambda attr:setattr(self,"status",True))
        # Searcn in the commands the STBY                   (REG 5)
        input_regular_exp["(STBY)"] = ("Operates the instrument",
                                          lambda attr:setattr(self,"status",False))
        # Searcn in the commands the STBY                   (REG 6)
        input_regular_exp["(STBY)"] = ("Operates the instrument",
                                          lambda attr:setattr(self,"status",False))
        # Searcn in the commands the STBY                   (REG 6)
        input_regular_exp["(STBY)"] = ("Operates the instrument",
                                          lambda attr:setattr(self,"status",False))

        ##########################################
        #### BLOCK 2: Search RE and set values ###
        ##########################################
        for expression in input_regular_exp.keys():
            # Search for command expression
            Match = re.search(expression,cmd)
            if Match != None:
                # Extract single expression
                single_cmd = cmd[Match.start():Match.end()]
                # Show command
                if self.log:
                    print(single_cmd)
                # Execute command
                input_regular_exp[expression][1](single_cmd)
        return self.messages

    def read(self):
        if self.status:
            time.sleep(3)
            x = np.float64(self.x)
            x = np.random.normal(x,x*0.000010)
            return f"{x} {self.unit},{self.frequency} HZ"
    def read_setting(self):
        if self.status:
            return (np.float64(self.x),self.unit,np.float64(self.frequency),"HZ")
        else:
            return (np.float64(0),"V",np.float64(0),"HZ")

class FLUKE_5500A:

    def __init__(self, bus_connection:str = "GPIB0",simulation = True):
        self.name = "FLUKE 5500A"

    compensation = {0:"None", 2:"WIRE2", 4:"WIRE4"} 
    def convertion(valor): 
        Prefijos = {"K":1E3,"M":1E6,"G":1E9,"m":1E-3,"uA":1E-6,"nA":1E-9,"V":1E0,"A":1E0,"OHM":1E0, "mV":1E-3, "mA":1E-3, "mF":1E-3, "uF":1E-6, "nF":1E-9, "pF":1E-12}
        if isinstance(valor, str):
            print(valor.split(" "))
            val,pref = valor.split(" ")
            val = int(val) * Prefijos[pref]
            return val
        elif isinstance(valor, float) or isinstance(valor, int) :
            val1 = valor
            return val1
    
    def set_DCV(self,amplitud_ch1,amplitud_ch2 = None):
        cha1 = self.convertion(amplitud_ch1)
        if amplitud_ch2 == None:
            self.send_visa_cmd(f"OUT {cha1} V")
        else:
            cha2 = self.convertion(amplitud_ch2)
            self.send_visa_cmd(f"OUT {cha1} V, {cha2} V")   
        return 0 

    def set_ACV(self,amplitud_ch1,frequencia,amplitud_ch2 = None)
        cha1 = self.convertion(amplitud_ch1)
        if amplitud_ch2 == None:
            self.send_visa_cmd(f"OUT {cha1} V, {frequencia} HZ")
        else:
            cha2 = self.convertion(amplitud_ch2)
            self.send_visa_cmd(f"OUT {cha1} V, {cha2} V,{frequencia} HZ")
        return 0

    def set_DCI(self,amplitud):
        amp = self.convertion(amplitud)
        self.send_visa_cmd(f"OUT {amp} A")   
        return 0

    def set_ACI(self,amplitud,frequencia):
        amp = self.convertion(amplitud)
        self.send_visa_cmd(f"OUT {amp} A, {frequencia} HZ") 
        return 0

    def set_OHM(self,amplitud,compensation = 0):
        amp = self.convertion(amplitud)
        if compensation == 2:
            self.send_visa_cmd(f"OUT {amp} OHM")
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        elif compensation == 4:
            self.send_visa_cmd(f"OUT {amp} OHM")
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        else:
            self.send_visa_cmd(f"OUT {amp} OHM")
        return 0 

    def set_CAP(self,amplitud,compensation = 0):
        amp = self.convertion(amplitud)
        if compensation == 2:
            self.send_visa_cmd(f"OUT {amp} F")
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        elif compensation == 4:
            self.send_visa_cmd(f"OUT {amp} F")
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        else:
            self.send_visa_cmd(f"OUT {amp} F")
        return 0 

    def set_RTD(self,amplitud,tipo = "PT385", compensation = 0):
        self.send_visa_cmd(f"TSENS_TYPE RTD")
        self.send_visa_cmd(f"RTD_TYPE {tipo}")
        if compensation == 2:
            self.send_visa_cmd(f"OUT {amplitud} CEL")
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        elif compensation == 4:
            self.send_visa_cmd(f"OUT {amplitud} CEL")
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        else:
            self.send_visa_cmd(f"OUT {amplitud} CEL")
        return 0 

    def set_TC(self,amplitud,tipo):
        self.send_visa_cmd(f"TSENS_TYPE TC")
        self.send_visa_cmd(f"TC_TYPE {tipo}")
        self.send_visa_cmd(f"OUT {amplitud} CEL")
        return 0 

    def set_TCMEAS(self,tipo):
        self.send_visa_cmd(f"TC_MEAS")
        self.send_visa_cmd(f"TC_TYPE {tipo}")

    


if __name__ == "__main__":
    Instrument = Fluke_5720A()
    Instrument.log = False 

    # Set output
    Instrument("OUT 1 V, 50 HZ")
    print(Instrument)
    print(Instrument.read())
    Instrument("operate")
    print(Instrument.read())
    Instrument("stby")
    print(f"Tipo {type(Instrument)}")

