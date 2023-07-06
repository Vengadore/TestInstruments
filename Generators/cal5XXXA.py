import pyvisa

# A device in the 5XXX scheme is meant to generate a value with an associated magnitude.
# We can imitate the behavior of a calibrator by knowing which commands it recieves and
# returning the expected value.


OPERATE_STATE = True


class FLUKE_5500A:

    def __init__(self, bus_connection: str = 'GPIB0::0::INSTR'):
        self.name = "FLUKE 5500A"
        self.compensation = {0: "None", 2: "WIRE2", 4: "WIRE4"}
        self.bus = bus_connection
        self.init_visa_connection()

    def init_visa_connection(self, termination_character="\r"):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus)
        self.inst.timeout = 5000
        return 0

    def disconnect(self):
        self.inst.close()

    def write(self, cmd: str):
        self.inst.write(cmd)
        self.inst.write("*WAI")
        return 0

    def operate(self):
        return self.inst.write("OPER")

    def stby(self):
        return self.inst.write("STBY")

    def reset(self):
        return self.inst.write("RST")

    def status(self):
        estado = self.inst.query("OPER?")
        estado = bool(estado.replace("\n", ""))
        return estado == OPERATE_STATE

    def convertion(self, valor):
        Prefijos = {"K": 1E3, "M": 1E6, "G": 1E9, "m": 1E-3, "uA": 1E-6, "nA": 1E-9, "V": 1E0,
                    "A": 1E0, "OHM": 1E0, "mV": 1E-3, "mA": 1E-3, "mF": 1E-3, "uF": 1E-6, "nF": 1E-9, "pF": 1E-12}
        if isinstance(valor, str):
            print(valor.split(" "))
            val, pref = valor.split(" ")
            val = float(val) * Prefijos[pref]
            return val
        elif isinstance(valor, float) or isinstance(valor, int):
            val1 = valor
            return val1

    def set_DCV(self, amplitud_ch1, amplitud_ch2=None):
        cha1 = self.convertion(amplitud_ch1)
        if amplitud_ch2 == None:
            self.write(f"OUT {cha1} V, 0 HZ")
        else:
            cha2 = self.convertion(amplitud_ch2)
            self.write(f"OUT {cha1} V, {cha2} V, 0 HZ")
        return 0

    def set_ACV(self, amplitud_ch1, frequencia, amplitud_ch2=None):
        cha1 = self.convertion(amplitud_ch1)
        if amplitud_ch2 == None:
            self.write(f"OUT {cha1} V, {frequencia} HZ")
        else:
            cha2 = self.convertion(amplitud_ch2)
            self.write(f"OUT {cha1} V, {cha2} V,{frequencia} HZ")
        return 0

    def set_DCI(self, amplitud):
        amp = self.convertion(amplitud)
        self.write(f"OUT {amp} A, 0 HZ")
        return 0

    def set_ACI(self, amplitud, frequencia):
        amp = self.convertion(amplitud)
        self.write(f"OUT {amp} A, {frequencia} HZ")
        return 0

    def set_OHM(self, amplitud, compensation=0):
        amp = self.convertion(amplitud)
        if compensation == 2:
            self.write(f"OUT {amp} OHM")
            self.write(f"ZCOMP {self.compensation[compensation]}")
        elif compensation == 4:
            self.write(f"OUT {amp} OHM")
            self.write(f"ZCOMP {self.compensation[compensation]}")
        else:
            self.write(f"OUT {amp} OHM")
            self.write(f"ZCOMP {self.compensation[compensation]}")
        return 0

    def set_CAP(self, amplitud, compensation=0):
        amp = self.convertion(amplitud)
        if compensation == 2:
            self.write(f"OUT {amp} F")
            self.write(f"ZCOMP {self.compensation[compensation]}")
        else:
            self.write(f"OUT {amp} F")
            self.write(f"ZCOMP {self.compensation[compensation]}")
        return 0

    def set_RTD(self, amplitud, tipo="PT385", compensation=0):
        self.write(f"TSENS_TYPE RTD")
        self.write(f"RTD_TYPE {tipo}")
        if compensation == 2:
            self.write(f"OUT {amplitud} CEL")
            self.write(f"ZCOMP {self.compensation[compensation]}")
        elif compensation == 4:
            self.write(f"OUT {amplitud} CEL")
            self.write(f"ZCOMP {self.compensation[compensation]}")
        else:
            self.write(f"OUT {amplitud} CEL")
            self.write(f"ZCOMP {self.compensation[compensation]}")
        return 0

    def set_TC(self, amplitud, tipo):
        self.write(f"TSENS_TYPE TC")
        self.write(f"TC_TYPE {tipo}")
        self.write(f"OUT {amplitud} CEL")
        return 0

    def set_TCMEAS(self, tipo):
        actual_meastc = self.inst.query("*TRG").split(",")[0]
        self.write(f"TC_TYPE {tipo}")
        return float(actual_meastc)

    def set_POWER_DC(self, amplitud_VCC, amplitud_ICC):
        aVCC = self.convertion(amplitud_VCC)
        aICC = self.convertion(amplitud_ICC)
        self.write(f"OUT {aVCC} V,{aICC} A")
        return 0

    def set_POWER_AC(self, amplitud_VCA, amplitud_ICA, frequencia):
        aVCA = self.convertion(amplitud_VCA)
        aICA = self.convertion(amplitud_ICA)
        self.write(f"OUT {aVCA} V,{aICA} A,{frequencia} HZ")
        return 0


class FLUKE_5720A(FLUKE_5500A):

    def __init__(self, bus_connection: str = 'GPIB0::0::INSTR'):
        super().__init__(bus_connection)
        self.name = "FLUKE 5720A"

    def set_DCV(self, amplitud_ch1, sense="OFF"):
        cha1 = self.convertion(amplitud_ch1)
        self.write(f"OUT {cha1} V, 0 HZ")
        self.write(f"EXTSENSE {sense}")
        return 0

    def set_ACV(self, amplitud_ch1, frequencia, sense="OFF"):
        cha1 = self.convertion(amplitud_ch1)
        self.write(f"EXTSENSE {sense}")
        self.write(f"OUT {cha1} V, {frequencia} HZ")
        return 0

    def set_DCI(self, amplitud, sense="OFF"):
        amp = self.convertion(amplitud)
        self.write(f"EXTSENSE {sense}")
        self.write(f"OUT {amp} A, 0 HZ")
        return 0

    def set_ACI(self, amplitud, frequencia, sense="OFF"):
        amp = self.convertion(amplitud)
        self.write(f"EXTSENSE {sense}")
        self.write(f"OUT {amp} A, {frequencia} HZ")
        return 0

    def set_OHM(self, amplitud, compensation=0):
        amp = self.convertion(amplitud)
        if compensation == 2:
            self.write(f"OUT {amp} OHM")
            self.write(f"RCOMP ON")
            self.write(f"EXTSENSE OFF")
        elif compensation == 4:
            self.write(f"OUT {amp} OHM")
            self.write(f"RCOMP OFF")
            self.write(f"EXTSENSE ON")
        else:
            self.write(f"OUT {amp} OHM")
            self.write(f"RCOMP OFF")
            self.write(f"EXTSENSE OFF")
        return 0
