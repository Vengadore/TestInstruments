import pyvisa
from visa_mock.base.base_mocker import BaseMocker, scpi
from visa_mock.base.register import register_resource

# A device in the 5XXX scheme is meant to generate a value with an associated magnitude.
# We can imitate the behavior of a calibrator by knowing which commands it recieves and
# returning the expected value.


OPERATE_STATE = True

class mock_fluke_5XXX(BaseMocker):
    def __init__(self, call_delay: float = 0):
        super().__init__(call_delay)
        self.set_initial_values()

    def set_initial_values(self):
        self.OUT1_amplitude = 0
        self.OUT1_units = "V"
        self.OUT2_amplitude = 0
        self.OUT2_units = ""
        self.frequency = 0
        self.available_units = ["V", "A", "DBM", "CEL", "FAR", "OHM"]
        self.FUNC = "DCV"
        self.available_FUNC = ["DCV", "ACV", "DCI", "ACI", "RES", "CAP", "RTD", "TC_OUT", "DC_POWER", "AC_POWER", "DCV_DCV", "ACV_ACV", "TC_MEAS"]
        self.ZCOMP = "NONE"
        self.RTD_TYPE = "PT385"
        self.TC_TYPE = "K"
        self.STATE = 0
        self.EXTSENSE = "OFF"
        self.ISR = 0

    @scpi("OPER<action>")
    def set_OPER(self, action: str) -> None:
        if action == "?":
            return self.STATE
        else:
            self.STATE = 1
        return None
    
    @scpi("STBY")
    def standby(self) -> None:
        self.STATE = 0
        return None

    @scpi("RST")
    def reset(self) -> None:
        self.set_initial_values()
        return None

    @scpi("FUNC?")
    def get_FUNC(self) -> str:
        return self.FUNC

    @scpi("OUT?")
    def get_OUT(self) -> str:
        if self.OUT2_units == "":
            return f"{self.OUT1_amplitude},{self.OUT1_units},{self.frequency}"
        else:
            return f"{self.OUT1_amplitude},{self.OUT1_units},{self.OUT2_amplitude},{self.OUT2_units},{self.frequency}"
    
    @scpi("OUT <primary_amplitude> DBM")
    def set_OUT(self, primary_amplitude: str) -> None:
        self.OUT1_amplitude = float(primary_amplitude)
        self.OUT1_units = "DBM"
        self.FUNC = "DC_POWER"
        return None
    
    @scpi("EXTSENSE <sense>")
    def set_EXTSENSE(self, sense: str) -> None:
        if sense in ["ON", "OFF"]:
            self.EXTSENSE = sense
            if sense == "ON":
                self.ISR |= (1<<2)
        return None
    
    @scpi("RCOMP <rcomp>")
    def set_RCOMP(self, rcomp: str) -> None:
        if rcomp in ["ON", "OFF"]:
            self.RCOMP = rcomp
            if rcomp == "ON":
                self.ISR |= (1<<4)
        return None
    
    @scpi("ISR?")
    def get_ISR(self) -> str:
        ISR = str(self.ISR)
        self.ISR = 0
        return str(ISR)

    @scpi("OUT <primary_amplitude> DBM, <frequency> HZ")
    def set_OUT(self, primary_amplitude: str, frequency: str) -> None:
        self.OUT1_amplitude = float(primary_amplitude)
        self.OUT1_units = "DBM"
        self.frequency = float(frequency)
        self.FUNC = "AC_POWER"
        return None
    
    @scpi("OUT <primary_amplitude> CEL")
    def set_OUT(self, primary_amplitude: str) -> None:
        self.OUT1_amplitude = float(primary_amplitude)
        self.OUT1_units = "CEL"
        self.FUNC = "RTD"
        return None
    
    @scpi("OUT <primary_amplitude> F")
    def set_OUT(self, primary_amplitude: str) -> None:
        self.OUT1_amplitude = float(primary_amplitude)
        self.OUT1_units = "FAR"
        self.FUNC = "CAP"
        return None

    @scpi("OUT <primary_amplitude> OHM")
    def set_OUT(self, primary_amplitude: str) -> None:
        self.OUT1_amplitude = float(primary_amplitude)
        self.OUT1_units = "OHM"
        self.FUNC = "RES"
        return None
    
    @scpi("OUT <primary_amplitude> <primary_units>, <frequency> HZ")
    def set_single_OUT(self, primary_amplitude: str, primary_units: str, frequency: str = "0") -> None:
        if self.OUT1_units not in self.available_units:
            raise Exception("Invalid units")
        self.OUT1_amplitude = float(primary_amplitude)
        self.OUT1_units = primary_units
        self.frequency = float(frequency)
    
        if self.OUT1_units == "V" and self.frequency == 0:
            self.FUNC = "DCV"
        elif self.OUT1_units == "V" and self.frequency != 0:
            self.FUNC = "ACV"
        elif self.OUT1_units == "A" and self.frequency == 0:
            self.FUNC = "DCI"
        elif self.OUT1_units == "A" and self.frequency != 0:
            self.FUNC = "ACI"
        elif self.OUT1_units == "OHM":
            self.FUNC = "RES"
        return None
    
    @scpi("ZCOMP <compensation>")
    def set_ZCOMP(self, compensation: str) -> None:
        if compensation in ["NONE", "WIRE2", "WIRE4"]:
            self.ZCOMP = compensation
        return None
    
    @scpi("ZCOMP?")
    def get_ZCOMP(self) -> str:
        return self.ZCOMP
    
    @scpi("TSENS_TYPE <type>")
    def set_TSENS_TYPE(self, type: str) -> None:
        if type in ["TC", "RTD"]:
            self.FUNC = type
        return None
    
    @scpi("TC_TYPE <type>")
    def set_TC_TYPE(self, type: str) -> None:
        if type in ["B", "C", "E", "J", "K", "N", "R", "S", "T", "X"]:
            self.TC_TYPE = type
        return None

    @scpi("TC_TYPE?")
    def get_TC_TYPE(self) -> str:
        return self.TC_TYPE
    
    @scpi("RTD_TYPE <type>")
    def set_RTD_TYPE(self, type: str) -> None:
        if type in ["PT385", "PT3926", "NI120"]:
            self.RTD_TYPE = type
        return None
    
    @scpi("RTD_TYPE?")
    def get_RTD_TYPE(self) -> str:
        return self.RTD_TYPE

    # TODO - This is a mess. We need to figure out how to handle multiple OUT commands
    #@scpi("OUT <primary_amplitude> <primary_units>, <secondary_amplitude> <secondary_units>, <frequency> HZ")
    #def set_OUT(self, primary_amplitude: str, primary_units: str, secondary_amplitude: str = "0", secondary_units: str = "", frequency: str = "0") -> None:
    #    if self.OUT1_units not in self.available_units or self.OUT2_units not in self.available_units:
    #        raise Exception("Invalid units")
    #    self.OUT1_amplitude = float(primary_amplitude)
    #    self.OUT1_units = primary_units
    #    self.OUT2_amplitude = float(secondary_amplitude)
    #    self.OUT2_units = secondary_units
    #    self.frequency = float(frequency)
    #    """
    #    <value> V
    #    <value> DBM
    #    <value> V, <value> Hz
    #    <value> DBM, <value> Hz
    #    <value> A
    #    <value> A, <value> Hz
    #    <value> OHM
    #    <value> F
    #    <value> CEL
    #    <value> FAR
    #    <value> HZ
    #    <value> V, <value> A
    #    <value> DBM, <value> A
    #    <value> V, <value> A, <value> HZ
    #    <value> DBM, <value> A, <value> HZ
    #    <value> V, <value> V
    #    <value> DBM, <value> DBM
    #    <value> V, <value> V, <value> HZ
    #    <value> DBM, <value> DBM, <value> HZ
    #    """
    #
    #    if self.OUT1_units == "V" and self.OUT2_units == "V":
    #        self.FUNC = "DCV_DCV"
    #    elif self.OUT1_units == "V" and self.OUT2_units == "A":
    #        self.FUNC = "DC_POWER"
    #    elif self.OUT1_units == "V" and self.OUT2_units == "" and self.frequency != 0:
    #        self.FUNC = "ACV"
    #    elif self.OUT1_units == "DBM" and self.OUT2_units == "" and self.frequency != 0:
    #        self.FUNC = "AC_POWER"
    #    elif self.OUT1_units == "A" and self.OUT2_units == "":
    #        self.FUNC = "DCI"
    #    elif self.OUT1_units == "A" and self.OUT2_units == "" and self.frequency != 0:
    #        self.FUNC = "ACI"
    #    
    #    return None
    
    @scpi("*WAI")
    def wait(self) -> None:
        pass


class FLUKE_5500A:

    def __init__(self,bus_connection: str = 'GPIB0::0::INSTR',
                      simulation: bool = False):
        self.name = "FLUKE 5500A"
        self.compensation = {0: "NONE", 2: "WIRE2", 4: "WIRE4"}
        self.bus = bus_connection
        self.SIM = simulation
        self.init_visa_connection()

    def init_visa_connection(self, termination_character="\r"):
        if self.SIM:
            register_resource(self.bus, mock_fluke_5XXX())
            rm = pyvisa.ResourceManager(visa_library="@mock")
        else:
            rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus, read_termination=termination_character)
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
        estado = estado.replace("\n", "") == "1"
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

    def __init__(self, bus_connection: str = 'GPIB0::0::INSTR', simulation: bool = False):
        super().__init__(bus_connection,simulation)
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
