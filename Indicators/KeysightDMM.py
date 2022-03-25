from ast import In
import pyvisa
from os import read
import numpy as np
import time
import re
from Generators import cal5XXXA


class Keysight_3458A:
    def __init__(self, bus_connection:str = "GPIB1",simulation = True):
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
        self.SIM = simulation
        if not self.SIM:
            self.init_visa_connection()

        ## Alcances
        self.alcances = {0:"100 mV",1:"1 V",
                         2:"10 V", 3:"100 V",
                         4:"1000 V"}
        self.alcancesRes= {0:"10 ",1:"100",2:"1000",3:"10000",4:"100000",5:"1000000",6:"10000000",7:"100000000",8:"1000000000"}
        self.alcancesA={0:"0.00001",1:"0.0001",2:"0.001",3:"0.01",4:"0.1",5:"1"}            
        self.resolutionFREQPER={0:"0.00001",1:"0.0001",2:"0.001",3:".01",4:".1"} ##Depende de la resolución es el tiempo y # de muestras.
    def __str__(self) -> str:
        return f"{self.name}:{self.bus}, {self.x} {self.unit}"

    def __name__(self):
        return "indicator"

    def init_visa_connection(self):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus, read_termination = "\r")
        self.inst.timeout = 40000
        return 0
    
    def reset(self):
        self.inst.write("RESET")
        return 0

    ## Set NPLC
    def SET_NPLC(self,NPLC : float = 10):
        self.inst.write(f"NPLC {NPLC}")
        return 0
    ## Set NDIG
    def SET_Ndig(self,Ndig : int = 8):
        self.inst.write(f"NDIG {Ndig}")
        return 0
    ## Set RES
    def SET_RES(self, Resolution : float = 0.000001):
        self.inst.write(f"RES {Resolution}")
        return 0
     ## Set OCOMP
    def SET_OCOMP(self, OCOMP ):
        self.inst.write(f"OCOMP {OCOMP}")
        return 0           
    ## DC
    def DCV(self,alcance : int = 1):
        if not self.SIM:
            self.inst.write(f"FUNC DCV {alcance}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0
    ## ACVSYNC
    def ACVSYNC(self,alcance : int = 1):
        if not self.SIM:
            self.inst.write(f"ACV {alcance}")
            self.inst.write("SETACV SYNC")
            self.SET_NPLC(100)
            self.SET_Ndig(8)
            self.inst.write("LFILTER ON") #? Se puede cambiar por funcion
            self.SET_RES(0.000001)
        return 0
    ## OHM
    def RESISTANCE(self,hilos,alcancesRes: int = 1):
        if not self.SIM:
            if hilos == "OHMF" :
                self.inst.write(f"FUNC OHMF {self.alcancesRes[alcancesRes]}")
                self.SET_Ndig(8)
                self.SET_NPLC(100)
                self.SET_OCOMP("ON")
            else :
                self.inst.write(f"FUNC OHM {self.alcancesRes[alcancesRes]}")
                self.SET_Ndig(8)
                self.SET_NPLC(300)
                self.SET_OCOMP("OFF")                     
        return 0  
    ## ACI
    def ACI(self,alcancesA: int = 1): 
        if not self.SIM:
            self.inst.write(f"FUNC ACI {self.alcancesA[alcancesA]}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0
    ## DCI
    def DCI(self,alcancesA: int = 1): 
        if not self.SIM:
            self.inst.write(f"FUNC DCI {self.alcancesA[alcancesA]}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0
    ## FREQ
    def FREQ(self,FSOURCE,resolutionFREQ: int = 1,intervalo: int = 1):
        if not self.SIM:
            if FSOURCE == "ACV":
                self.inst.write(f"FUNC FREQ {self.alcances[intervalo]},{resolutionFREQPER[resolutionFREQ]}")
                self.inst.write("FSOURCE ACV")
            else:
                self.inst.write(f"FUNC FREQ {self.alcances[intervalo]},{resolutionFREQPER[resolutionFREQ]}")
                self.inst.write("FSOURCE ACI")    
        return 0  
    ## PER
    def PER(self,FSOURCE,resolutionFREQ: int = 1,intervalo: int = 1):
        if not self.SIM:
            if FSOURCE == "ACV":
                self.inst.write(f"FUNC PER {self.alcances[intervalo]},{resolutionFREQPER[resolutionFREQ]}")
                self.inst.write("FSOURCE ACV")
            else:
                self.inst.write(f"FUNC PER {self.alcances[intervalo]},{resolutionFREQPER[resolutionFREQ]}")
                self.inst.write("FSOURCE ACI")    
        return 0        
    ## Sample
    def SAMPLE(self,N_samples : int = 1):
        Samples = []
        for i in range(N_samples):
            self.inst.write("TRIG SGL")
            lectura = self.inst.read()
            lectura = float(lectura)
            Samples.append(lectura)
        return Samples
    def __call__(self, indicator:cal5XXXA.Fluke_5720A) -> str:
        # The basic operation of the multímeter is to performa reading from an external source
        if indicator.__name__ == "generator":
            # simulate wait time
            time.sleep(4)
            x,unit,frequency,frq_unit = indicator.read_setting()
            if unit not in ["V","A","OHM"]:
                print("ERROR, MAGNITUDE NOT SUPPORTED!!")
                return 1
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
            return 1
            

if __name__ == "__main__":
    Instrument = cal5XXXA.Fluke_5720A()
    Reader = Keysight_3458A()
    Instrument.log = False

    Reader.DCV(10)
    Reader.SAMPLE(10)

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
    
