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

