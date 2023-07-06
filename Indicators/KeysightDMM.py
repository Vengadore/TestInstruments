import pyvisa

class Keysight_3458A:
    def __init__(self, bus_connection: str = 'GPIB0::1::INSTR', simulation=False):
        self.name = "Keysight 3458A"
        self.bus = bus_connection
        self.SN = 95902492
        self.FWrev = "1.00"
        self.status = False  # True = OPERATE <> False = STBY
        self.Magnitudes = ["V", "A", "OHM"]
        self.x = "0"
        self.unit = "V"
        self.frequency = "0"
        # This is the default value of the multimeter
        self.set_measurement_functions("DCV")
        self.log = False
        self.SIM = simulation
        if not self.SIM:
            self.init_visa_connection()

        # Alcances
        ##self.alcancesDCVACV = {0:"10 mV",1:"100 mV",2:"1 V",3:"10 V", 4:"100 V",5:"1000 V"}
        ##self.alcancesOHM = {0:"10 OHM",1:"100 OHM",2:"1 KOHM",3:"10 KOHM",4:"100 KOHM",5:"1 MOHM",6:"10 MOHM",7:"100 MOHM",8:"1 GOHM"}
        ##self.alcancesDCIACI = {0:"10 uA",1:"100 uA",2:"1 mA",3:"10 mA",4:"100 mA",5:"1 A"}
        # self.resolutionFREQPER = {0:"0.00001",1:"0.0001",2:"0.001",3:".01",4:".1"} ##Depende de la resolución es el tiempo y # de muestras.

    def __str__(self) -> str:
        return f"{self.name}:{self.bus}, {self.x} {self.unit}"

    def set_measurement_functions(self, Function):
        FUNCTION = {1: "DCV", 2: "ACV", 3: "ACDCV", 4: "OHM",
                    5: "OHMF", 6: "DCI", 7: "ACI", 8: "ACDCI",
                    9: "FREQ", 10: "PER", 11: "DSAC", 12: "DSDC",
                    13: "SSAC", 14: "SSDC"}
        # Change keys for values
        self.MeasurementFunction = res = dict(
            (v, k) for k, v in FUNCTION.items())[Function]

    def __name__(self):
        return "indicator"

    def init_visa_connection(self, termination_character="\r"):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(
            self.bus, read_termination=termination_character)
        self.inst.timeout = 40000
        return 0

    def query(self, cmd: str):
        if self.SIM:
            return "1, 0"
        else:
            self.inst.query(cmd)

    def reset(self):
        self.inst.write("RESET")
        return 0

    def SET_NPLC(self, NPLC: float = 10):
        self.inst.write(f"NPLC {NPLC}")
        return 0

    def SET_Ndig(self, Ndig: int = 8):
        self.inst.write(f"NDIG {Ndig}")
        return 0

    def SET_RES(self, Resolution: float = 0.000001):
        self.inst.write(f"RES {Resolution}")
        return 0

    def SET_OCOMP(self, OCOMP):
        self.inst.write(f"OCOMP {OCOMP}")
        return 0

    def convertion(self, valor):
        Prefijos = {"K": 1E3, "M": 1E6, "G": 1E9, "m": 1E-3, "uA": 1E-6,
                    "nA": 1E-9, "V": 1E0, "A": 1E0, "OHM": 1E0, "mV": 1E-3, "mA": 1E-3}
        if isinstance(valor, str):
            print(valor.split(" "))
            val, pref = valor.split(" ")
            val = int(val) * Prefijos[pref]
            return val
        elif isinstance(valor, float) or isinstance(valor, int):
            val1 = valor
            return val1

    def DCV(self, alcanceDCV = "100 m"):
        if not self.SIM:
            ranges = self.convertion(alcanceDCV)
            self.inst.write(f"FUNC DCV {ranges}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0

    def ACVSYNC(self, alcanceACVSYNC = "10 m"):
        if not self.SIM:
            ranges = self.convertion(alcanceACVSYNC)
            self.inst.write(f"ACV {ranges}")
            self.inst.write("SETACV SYNC")
            self.SET_NPLC(100)
            self.SET_Ndig(8)
            self.inst.write("LFILTER ON")  # ? Se puede cambiar por funcion
            self.SET_RES(0.000001)
        return 0

    def OHM(self, hilos, alcanceOHM = "10 OHM"):
        if not self.SIM:
            ranges = self.convertion(alcanceOHM)
            if hilos == "OHMF":
                self.inst.write(f"FUNC OHMF {ranges}")
                self.SET_Ndig(8)
                self.SET_NPLC(100)
                self.SET_OCOMP("ON")
            else:
                self.inst.write(f"FUNC OHM {ranges}")
                self.SET_Ndig(8)
                self.SET_NPLC(300)
                self.SET_OCOMP("OFF")
        return 0

    def ACI(self, alcanceACI = "100 uA"):
        if not self.SIM:
            ranges = self.convertion(alcanceACI)
            self.inst.write(f"FUNC ACI {ranges}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0

    def DCI(self, alcanceDCI = "100 uA"):
        if not self.SIM:
            ranges = self.convertion(alcanceDCI)
            self.inst.write(f"FUNC DCI {ranges}")
            self.SET_Ndig(8)
            self.SET_NPLC(100)
        return 0

    def FREQ(self, FSOURCE, resolutionFREQPER: float = 0.00001, alcanceACVorACI = "100 m"):
        ranges = self.convertion(alcanceACVorACI)
        if FSOURCE == "ACV":
            self.inst.write("FSOURCE ACV")
            self.inst.write(f"FUNC FREQ {ranges},{resolutionFREQPER}")
        else:
            self.inst.write("FSOURCE ACI")
            self.inst.write(f"FUNC FREQ {ranges},{resolutionFREQPER}")
        return 0

    def PER(self, FSOURCE, resolutionFREQPER, alcanceACVorACI = "100 m"):
        if not self.SIM:
            ranges = self.convertion(alcanceACVorACI)
            if FSOURCE == "ACV":
                self.inst.write("FSOURCE ACV")
                self.inst.write(f"FUNC PER {ranges},{resolutionFREQPER}")
            else:
                self.inst.write("FSOURCE ACI")
                self.inst.write(f"FUNC PER {ranges},{resolutionFREQPER}")
            return 0

    def SAMPLE(self, N_samples: int = 1):
        Samples = []
        self.inst.write("NRDGS 1, AUTO")
        for i in range(N_samples):
            self.inst.write("TRIG SGL")
            lectura = self.inst.read()
            lectura = float(lectura)
            Samples.append(lectura)
        return Samples
