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
        self.set_measurement_functions("DCV") # This is the default value of the multimeter
        self.log = False
        self.SIM = simulation
        if not self.SIM:
            self.init_visa_connection()

        ## Alcances
        self.alcancesDCVACV = {0:"10 mV",1:"100 mV",2:"1 V",3:"10 V", 4:"100 V",5:"1000 V"}
        self.alcancesOHM = {0:"10 OHM",1:"100 OHM",2:"1 KOHM",3:"10 KOHM",4:"100 KOHM",5:"1 MOHM",6:"10 MOHM",7:"100 MOHM",8:"1 GOHM"}
        self.alcancesDCIACI = {0:"10 uA",1:"100 uA",2:"1 mA",3:"10 mA",4:"100 mA",5:"1 A"}            
        self.resolutionFREQPER = {0:"0.00001",1:"0.0001",2:"0.001",3:".01",4:".1"} ##Depende de la resolución es el tiempo y # de muestras.

        Prefijos = {"KOHM":1E3,"MOHM":1E6,"GOHM":1E9,"mV":1E-3,"mA":1E-3,"uA":1E-6,"nA":1E-9,"V":1E0,"A":1E0,"OHM":1E0}

    def __str__(self) -> str:
        return f"{self.name}:{self.bus}, {self.x} {self.unit}"

    def set_measurement_functions(self,Function):
        FUNCTION = {1:"DCV",2:"ACV",3:"ACDCV",4:"OHM",
                    5:"OHMF",6:"DCI",7:"ACI",8:"ACDCI",
                    9:"FREQ",10:"PER",11:"DSAC",12:"DSDC",
                    13:"SSAC",14:"SSDC"}
        #Change keys for values
        self.MeasurementFunction = res = dict((v,k) for k,v in FUNCTION.items())[Function]

    def __name__(self):
        return "indicator"

    def init_visa_connection(self):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus, read_termination = "\r")
        self.inst.timeout = 40000
        return 0

    def query(self,cmd):
        if self.SIM:
            return "1, 0"
        else:
            self.inst.query(cmd)
    
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

    ## Traducción de Prefijos
    def convertion(self,valor):
        print(valor.split(" "))
        val,pref = valor.split(" ")
        val = int(val) * Prefijos[pref]
        return val

    ## DC
    def DCV(self,alcanceDCV : int = 1):
        if not self.SIM:
            ranges=convertion(alcanceDCV)
            self.inst.write(f"FUNC DCV {ranges}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0
    ## ACVSYNC
    def ACVSYNC(self,alcanceACVSYNC : int = 1):
        if not self.SIM:
            ranges=convertion(alcanceACVSYNC)
            self.inst.write(f"ACV {ranges}")
            self.inst.write("SETACV SYNC")
            self.SET_NPLC(100)
            self.SET_Ndig(8)
            self.inst.write("LFILTER ON") #? Se puede cambiar por funcion
            self.SET_RES(0.000001)
        return 0
    ## OHM
    def OHM(self,hilos,alcanceOHM: int = 1):
        if not self.SIM:
            ranges=convertion(alcanceOHM)
            if hilos == "OHMF" :
                self.inst.write(f"FUNC OHMF {ranges}")
                self.SET_Ndig(8)
                self.SET_NPLC(100)
                self.SET_OCOMP("ON")
            else :
                self.inst.write(f"FUNC OHM {ranges}")
                self.SET_Ndig(8)
                self.SET_NPLC(300)
                self.SET_OCOMP("OFF")                     
        return 0  
    ## ACI
    def ACI(self,alcanceACI: int = 1): 
        if not self.SIM:
            ranges=convertion(alcanceACI)
            self.inst.write(f"FUNC ACI {ranges}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0
    ## DCI
    def DCI(self,alcanceDCI: int = 1): 
        if not self.SIM:
            ranges=convertion(alcanceDCI)
            self.inst.write(f"FUNC DCI {ranges}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0
    ## FREQ
    def FREQ(self,FSOURCE,resolutionFREQPER,alcanceACVorACI: int = 1):
            ranges=convertion(alcanceACVorACI)
            if FSOURCE == "ACV":          
                self.inst.write("FSOURCE ACV")
                self.inst.write(f"FUNC FREQ {ranges},{self.resolutionFREQPER[resolutionFREQPER]}")
            else:
                self.inst.write("FSOURCE ACI")  
                self.inst.write(f"FUNC FREQ {ranges},{self.resolutionFREQPER[resolutionFREQPER]}")  
            return 0  
    ## PER
    def PER(self,FSOURCE,resolutionFREQPER,alcanceACVorACI: int = 1):
        if not self.SIM:
            ranges=convertion(alcanceACVorACI)
            if FSOURCE == "ACV":
                self.inst.write("FSOURCE ACV")
                self.inst.write(f"FUNC PER {ranges},{self.resolutionFREQPER[resolutionFREQPER]}")
            else:
                self.inst.write("FSOURCE ACI") 
                self.inst.write(f"FUNC PER {ranges},{self.resolutionFREQPER[resolutionFREQ]}")   
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
    
