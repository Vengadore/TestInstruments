import pyvisa
from visa_mock.base.base_mocker import BaseMocker, scpi
from visa_mock.base.register import register_resource

class mock_Keysight_3458A(BaseMocker):
    def __init__(self, call_delay: float = 0):
        super().__init__(call_delay)
        self.available_functions = {"DCV": 1, "ACV": 2, "ACDCV": 3, "OHM": 4,
                                    "OHMF": 5, "DCI": 6, "ACI": 7, "ACDCI": 8,
                                    "FREQ": 9, "PER": 10, "DSAC": 11, "DSDC": 12,
                                    "SSAC": 13, "SSDC": 14}
        self.function = "DCV"
        self.range = "0.1"
        self.integration_time = 10
        self.number_of_readings = 1
        self.trigger_type = "SGL"
        self.digits = 8
        self.OCOMP = "ON"
        self.LFILTER = "OFF"
        self.RES = 0.000001

    @scpi("FUNC?")
    def idn(self) -> str: 
        """
        'FUNC'
        """
        return str(self.available_functions[self.function]) + ", " + str(self.range) + " "
    
    @scpi("FUNC <function> <range>")
    def set_function(self, function: str, range: str) -> None:
        """
        'FUNC {function} {range}'
        """
        if function not in self.available_functions:
            raise ValueError(f"Function {function} not available")
        else:
            self.function = function
            self.range = range

    @scpi("NPLC?")
    def get_integration_time(self) -> float:
        """
        'NPLC'
        """
        return str(self.integration_time)
    
    @scpi("NPLC <integration_time>")
    def set_integration_time(self, integration_time: str) -> None:
        """
        'NPLC {integration_time}'
        """
        self.integration_time =float(integration_time)

    @scpi("NRDGS?")
    def get_number_of_readings(self) -> int:
        """
        'NRDGS'
        """
        return str(self.number_of_readings)
    
    @scpi("NRDGS <number_of_readings>, AUTO")
    def set_number_of_readings(self, number_of_readings: str) -> None:
        """
        'NRDGS {number_of_readings}'
        """
        self.number_of_readings = int(number_of_readings)

    @scpi("TRIG?")
    def get_trigger(self) -> str:
        """
        'TRIG'
        """
        return self.trigger_type
    
    @scpi("TRIG <trigger_type>")
    def trigger(self, trigger_type:str) -> None:
        """
        'TRIG SGL'
        """
        self.trigger_type = trigger_type
    
    @scpi("NDIG?")
    def get_digits(self) -> int:
        """
        'NDIG'
        """
        return str(self.digits)
    
    @scpi("NDIG <digits>")
    def set_digits(self, digits: str) -> None:
        """
        'NDIG {digits}'
        """
        self.digits = int(digits)

    @scpi("OCOMP <OCOMP>")
    def set_open_compensation(self, OCOMP: str) -> None:
        """
        'OCOMP {OCOMP}'
        """
        self.OCOMP = OCOMP

    @scpi("SETACV <SETACV>")
    def set_AC_voltage(self, SETACV: str) -> None:
        """
        'SETACV {SETACV}'
        """
        self.SETACV = SETACV
    
    @scpi("LFILTER <LFILTER>")
    def set_filter(self, LFILTER: str) -> None:
        """
        'LFILTER {LFILTER}'
        """
        self.LFILTER = LFILTER

    @scpi("RES <RES>")
    def set_resolution(self, RES: str) -> None:
        """
        'RES {RES}'
        """
        self.RES = float(RES)

    @scpi("RES?")
    def get_resolution(self) -> str:
        """
        'RES'
        """
        return str(self.RES)

class Keysight_3458A:
    """
    Class representing the Keysight 3458A Digital Multimeter.

    Attributes:
        name (str): The name of the multimeter.
        bus (str): The bus connection of the multimeter.
        SN (int): The serial number of the multimeter.
        FWrev (str): The firmware revision of the multimeter.
        status (bool): The status of the multimeter (True = OPERATE, False = STBY).
        Magnitudes (list): The supported measurement magnitudes.
        x (str): The current measurement value.
        unit (str): The unit of the current measurement value.
        frequency (str): The frequency of the measurement.
        log (bool): Flag indicating whether to log the measurements.
        SIM (bool): Flag indicating whether the multimeter is in simulation mode.

    Methods:
        __init__(bus_connection: str = 'GPIB0::1::INSTR', simulation=False): Initializes the Keysight_3458A object.
        __str__(): Returns a string representation of the multimeter.
        set_measurement_functions(Function): Sets the measurement function of the multimeter.
        init_visa_connection(termination_character="\r"): Initializes the VISA connection to the multimeter.
        query(cmd: str): Sends a query command to the multimeter and returns the response.
        reset(): Resets the multimeter.
        SET_NPLC(NPLC: float = 10): Sets the integration time of the multimeter.
        SET_Ndig(Ndig: int = 8): Sets the number of digits for the measurement.
        SET_RES(Resolution: float = 0.000001): Sets the resolution of the multimeter.
        SET_OCOMP(OCOMP): Sets the open compensation mode of the multimeter.
        convertion(valor): Converts a measurement value to the appropriate format.
        DCV(alcanceDCV = "100 m"): Sets the multimeter to DC voltage measurement mode.
        ACVSYNC(alcanceACVSYNC = "10 m"): Sets the multimeter to AC voltage measurement mode with synchronous filtering.
        OHM(hilos, alcanceOHM = "10 OHM"): Sets the multimeter to resistance measurement mode.
        ACI(alcanceACI = "100 uA"): Sets the multimeter to AC current measurement mode.
        DCI(alcanceDCI = "100 uA"): Sets the multimeter to DC current measurement mode.
        FREQ(FSOURCE, resolutionFREQPER: float = 0.00001, alcanceACVorACI = "100 m"): Sets the multimeter to frequency measurement mode.
        PER(FSOURCE, resolutionFREQPER, alcanceACVorACI = "100 m"): Sets the multimeter to period measurement mode.
        SAMPLE(N_samples: int = 1): Performs multiple measurements and returns the results as a list.
    """
    def __init__(self, bus_connection: str = 'GPIB0::1::INSTR', simulation=False):
        """
        Initializes the Keysight_3458A object.

        Args:
            bus_connection (str): The bus connection of the multimeter.
            simulation (bool): Flag indicating whether the multimeter is in simulation mode.
        """
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
        self.init_visa_connection()

    def __str__(self) -> str:
        """
        Returns a string representation of the multimeter.

        Returns:
            str: The string representation of the multimeter.
        """
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
        if self.SIM:
            register_resource(self.bus, mock_Keysight_3458A())
            rm = pyvisa.ResourceManager(visa_library="@mock")
        else:
            rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.bus, read_termination=termination_character)
        self.inst.timeout = 40000
        return 0

    def query(self, cmd: str):
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

    def convertion(self, valor) -> float:
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
        ranges = self.convertion(alcanceDCV)
        self.inst.write(f"FUNC DCV {ranges}")
        self.SET_Ndig(8)
        self.SET_NPLC(100)
        return 0

    def ACVSYNC(self, alcanceACVSYNC = "10 m"):
        ranges = self.convertion(alcanceACVSYNC)
        self.inst.write(f"FUNC ACV {ranges}")
        self.inst.write("SETACV SYNC")
        self.SET_NPLC(100)
        self.SET_Ndig(8)
        self.inst.write("LFILTER ON")  # ? Se puede cambiar por funcion
        self.SET_RES(0.000001)
        return 0

    def OHM(self, hilos, alcanceOHM = "10 OHM"):
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
        ranges = self.convertion(alcanceACI)
        self.inst.write(f"FUNC ACI {ranges}")
        self.SET_Ndig(8)
        self.SET_NPLC(100)
        return 0

    def DCI(self, alcanceDCI = "100 uA"):
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
            lectura = self.inst.read() if not self.SIM else "0.00000000E+00"
            lectura = float(lectura)
            Samples.append(lectura)
        return Samples


if __name__ == "__main__":
    register_resource("MOCK0::mock1::INSTR", mock_Keysight_3458A())
    rc = pyvisa.ResourceManager(visa_library="@mock")
    res = rc.open_resource("MOCK0::mock1::INSTR") 
    print(res.query("FUNC?"))

    res.write("FUNC DCV 0.1")

    multimetro = Keysight_3458A("MOCK0::mock1::INSTR", simulation=True)
    multimetro.DCV("1 V")
    multimetro.inst.write("FUNC ACV 0.1")
    print(multimetro.SAMPLE(10))
