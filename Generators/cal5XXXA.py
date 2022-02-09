import numpy as np
import time
import re
# A device in the 5XXX scheme is meant to generate a value with an associated magnitude.
# We can imitate the behavior of a calibrator by knowing which commands it recieves and
# returning the expected value.

class Fluke_5720A:
    def __init__(self, bus_connection:str = "GPIB0"):
        self.name = "FLUKE 5720A"
        self.bus = bus_connection
        self.SN = 829848492
        self.FWrev = "1.01b"
        self.status = False # True = OPERATE <> False = STBY
        self.Magnitudes = ["V","A","DB","DMB","OHM"]
        self.x = "0"
        self.unit = "V"
        self.frequency = "0"
    def __str__(self) -> str:
        return f"{self.name}:{self.bus}, {self.x} {self.unit}, {self.frequency} HZ"
    def __call__(self, cmd:str) -> str:
        # Capitalize the whole string
        cmd = cmd.upper()

        ####################################
        ### BLOCK 1: regular expressions ###
        ####################################
        # Search in the command the setting for the output  (REG 1)
        temp1 = "|".join([i for i in self.Magnitudes])
        output1_reg = "(OUT [0-9]{1,3} (" + temp1 + "))"
        # Search in the command the frequency               (REG 2)
        output2_reg = "([0-9]{1,5} HZ)"
        # Searcn in the commands the IDN                    (REG 3)
        output3_reg = "(\*IDN\?)"
        # Searcn in the commands the OPERATE                (REG 4)
        output4_reg = "(OPERATE)"
        # Searcn in the commands the STBY                   (REG 5)
        output5_reg = "(STBY)"
        
        message = ""

        #########################################
        ### BLOCK 2: Search RE and set values ###
        #########################################
        ## ---- Search for the setting to set the output ----
        Match = re.search(output1_reg,cmd)
        if Match != None:
            _,self.x,self.unit = cmd[Match.start():Match.end()].split(" ")
        ## ---- Search for the setting to set the frequency ----
        Match = re.search(output2_reg,cmd)
        if Match != None:
            self.frequency = cmd[Match.start():Match.end()].split(" ")
        ## ---- Search for the command for IDN ----
        Match = re.search(output3_reg,cmd)
        if Match != None:
            self.frequency = cmd[Match.start():Match.end()].split(" ")
            message += f"IDN:{self.name},SN:{self.SN},FWrev:{self.FWrev}"
        ## ---- Search for the operate command ----
        Match = re.search(output4_reg,cmd)
        if Match != None:
            self.status = True
        ## ---- Search for the standby command ----
        Match = re.search(output5_reg,cmd)
        if Match != None:
            self.status = False
        return message
    def read(self):
        if self.status:
            time.sleep(3)
            x = np.float(self.x)
            x = np.random.normal(x,x*0.000010)
            return f"{x} {self.unit},{self.frequency} HZ"

