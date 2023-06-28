from os import lseek
import pyvisa

# A device in the 5XXX scheme is meant to generate a value with an associated magnitude.
# We can imitate the behavior of a calibrator by knowing which commands it recieves and
# returning the expected value.


OPERATE_STATE = True


class FLUKE_5500A:

    def __init__(self, indice = 0):
        self.name = "FLUKE 5500A"
        self.compensation = {0:"None", 2:"WIRE2", 4:"WIRE4"}
        self.indice = indice
        self.seleccionarGPIB()

    def init_visa_connection(self):
        rm=pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus)
        self.inst.timeout = 5000
        return 1
    
    def disconnect(self):
        self.inst.close()

    def seleccionarGPIB (self):
        rm=pyvisa.ResourceManager()
        bus_connection=rm.list_resources()
        self.bus=bus_connection[self.indice]
        self.init_visa_connection()
        return 1

    def send_visa_cmd(self,cmd):
        self.inst.write(cmd)
        self.inst.write("*WAI")
        return 1
    
    def operate(self):
        return self.inst.write("OPER")

    def stby(self):
        return self.inst.write("STBY")
    
    def status(self):
        estado = self.inst.query("OPER?")
        estado = bool(estado.replace("\n",""))
        return estado == OPERATE_STATE

    def convertion(self,valor): 
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
            self.send_visa_cmd(f"OUT {cha1} V, 0 HZ")
        else:
            cha2 = self.convertion(amplitud_ch2)
            self.send_visa_cmd(f"OUT {cha1} V, {cha2} V, 0 HZ")
        return 0 

    def set_ACV(self,amplitud_ch1,frequencia,amplitud_ch2 = None):
        cha1 = self.convertion(amplitud_ch1)
        if amplitud_ch2 == None:
            self.send_visa_cmd(f"OUT {cha1} V, {frequencia} HZ")
        else:
            cha2 = self.convertion(amplitud_ch2)
            self.send_visa_cmd(f"OUT {cha1} V, {cha2} V,{frequencia} HZ")
        return 0

    def set_DCI(self,amplitud):
        amp = self.convertion(amplitud)
        self.send_visa_cmd(f"OUT {amp} A, 0 HZ")   
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
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        return 0 

    def set_CAP(self,amplitud,compensation = 0):
        amp = self.convertion(amplitud)
        if compensation == 2:
            self.send_visa_cmd(f"OUT {amp} F")
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        else:
            self.send_visa_cmd(f"OUT {amp} F")
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
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
            self.send_visa_cmd(f"ZCOMP {self.compensation[compensation]}")
        return 0 

    def set_TC(self,amplitud,tipo):
        self.send_visa_cmd(f"TSENS_TYPE TC")
        self.send_visa_cmd(f"TC_TYPE {tipo}")
        self.send_visa_cmd(f"OUT {amplitud} CEL")
        return 0 

    def set_TCMEAS(self,tipo):
        actual_meastc = self.inst.query("*TRG").split(",")[0]
        self.send_visa_cmd(f"TC_TYPE {tipo}")
        return float(actual_meastc)

    def set_POWER_DC(self,amplitud_VCC,amplitud_ICC):
         aVCC= self.convertion(amplitud_VCC)
         aICC= self.convertion(amplitud_ICC)
         self.send_visa_cmd(f"OUT {aVCC} V,{aICC} A")
         return 0

    def set_POWER_AC(self,amplitud_VCA,amplitud_ICA,frequencia):
         aVCA= self.convertion(amplitud_VCA)
         aICA= self.convertion(amplitud_ICA)
         self.send_visa_cmd(f"OUT {aVCA} V,{aICA} A,{frequencia} HZ")
         return 0

class FLUKE_5720A(FLUKE_5500A):
    
    def __init__(self):
        super().__init__()
        self.name = "FLUKE 5720A"
        self.seleccionarGPIB()

    def set_DCV(self,amplitud_ch1,sense = "OFF"):
        cha1 = self.convertion(amplitud_ch1)
        self.send_visa_cmd(f"OUT {cha1} V, 0 HZ")
        self.send_visa_cmd(f"EXTSENSE {sense}")
        return 0 

    def set_ACV(self,amplitud_ch1,frequencia,sense = "OFF"):
        cha1 = self.convertion(amplitud_ch1)
        self.send_visa_cmd(f"EXTSENSE {sense}")
        self.send_visa_cmd(f"OUT {cha1} V, {frequencia} HZ")
        return 0

    def set_DCI(self,amplitud,sense = "OFF"):
        amp = self.convertion(amplitud)
        self.send_visa_cmd(f"EXTSENSE {sense}")
        self.send_visa_cmd(f"OUT {amp} A, 0 HZ")   
        return 0

    def set_ACI(self,amplitud,frequencia,sense = "OFF"):
        amp = self.convertion(amplitud)
        self.send_visa_cmd(f"EXTSENSE {sense}")
        self.send_visa_cmd(f"OUT {amp} A, {frequencia} HZ") 
        return 0

    def set_OHM(self,amplitud,compensation = 0):
        amp = self.convertion(amplitud)
        if compensation == 2:
            self.send_visa_cmd(f"OUT {amp} OHM")
            self.send_visa_cmd(f"RCOMP ON")
            self.send_visa_cmd(f"EXTSENSE OFF")
        elif compensation == 4:
            self.send_visa_cmd(f"OUT {amp} OHM")
            self.send_visa_cmd(f"RCOMP OFF")
            self.send_visa_cmd(f"EXTSENSE ON")
        else:
            self.send_visa_cmd(f"OUT {amp} OHM")
            self.send_visa_cmd(f"RCOMP OFF")
            self.send_visa_cmd(f"EXTSENSE OFF")
        return 0 

if __name__ == "__main__":
    Instrument = FLUKE_5720A()
    Instrument.log = False 

    # Set output
    Instrument("OUT 1 V, 50 HZ")
    print(Instrument)
    print(Instrument.read())
    Instrument("operate")
    print(Instrument.read())
    Instrument("stby")
    print(f"Tipo {type(Instrument)}")

