from ast import In
from os import read
import numpy as np
import time
import re
from Generators import cal5XXXA


class Keysight_3458A:
    def __init__(self, bus_connection:str = "GPIB1"):
        self.name = "Keysight 3458A"
        self.bus = bus_connection
        self.SN = 95902492
        self.FWrev = "1.00"
        self.status = False # True = OPERATE <> False = STBY
        self.Magnitudes = ["V","A","OHM"]
        self.x = "0"
        self.unit = "V"
        self.frequency = "0"
        self.log = False
    def __str__(self) -> str:
        return f"{self.name}:{self.bus}, {self.x} {self.unit}"

    def __name__(self):
        return "indicator"
    
    def __call__(self, indicator:cal5XXXA.Fluke_5720A) -> str:
        # The basic operation of the multímeter is to performa reading from an external source
        if indicator.__name__ == "generator":
            # simulate wait time
            time.sleep(4)
            x,unit,frequency,frq_unit = indicator.read_setting()
            if unit not in ["V","A","OHM"]:
                print("ERROR, MAGNITUDE NOT SUPPORTED!!")
                return 0
            if unit == "OHM":
                frequency = 0
            if frequency == 0:
                frq_unit = ""
            if unit == "A":
                unit = "I"
            if frequency > 0:
                unit += "AC"
            reading = np.random.normal(x,x*10E-6)
            reading = np.round(reading,7)

            return f"{reading} {unit}"
        else:
            print("YOU CAN'T READ FROM THIS DEVICE")
            return 0
            

if __name__ == "__main__":
    Instrument = cal5XXXA.Fluke_5720A()
    Reader = Keysight_3458A()
    Instrument.log = False

    # Set output
    Instrument("OUT 1 V, 0 HZ")
    Instrument("operate")
    print(Reader(Instrument))
    Instrument("stby")
    print(Reader(Instrument))
    Instrument("OUT 120 OHM")
    print(Reader(Instrument))
    Instrument("operate")
    print(Reader(Instrument))
    Instrument("OUT 20 A, 10 HZ")
    print(Reader(Instrument))
    
