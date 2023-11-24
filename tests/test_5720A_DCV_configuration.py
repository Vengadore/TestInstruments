from Generators.cal5XXXA import *
import unittest
import time


# Test parameters
SIMULATION = True
LOGS = True

# Test functions


def log(message):
    if LOGS:
        print(message)


class CalibratorConfiguration:
    def __init__(self) -> None:
        self.device = object
    # Constats for test
    FUNCTION = {'DCV': "DCV", 'ACV': "ACV", 'DCI': "DCI", 'ACI': "ACI",
                'RES': "RES", 'CAP': "CAP", 'RTD': "RTD", 'TC_OUT': "TC_OUT",
                'DC_POWER': "DC_POWER", 'AC_POWER': "AC_POWER", 'DCV_DCV': "DCV_DCV", 'ACV_ACV': "ACV_ACV", 'TC_MEAS': "TC_MEAS"}

    # Available tests
#   AMPLITUDE_P
#   MAGNITUDE_GENERATED_P
#   RANGE_P
#   FREQUENCY

    def test_configuration(self, configuration: dict):
        map_tests = {"AMPLITUDE_P1": self.Amplitude_P1,
                     "FREQUENCY": self.Frequency,
                     "ZCOMP": self.Zcomp,
                     "GENERATE_FUNCTION": self.Generate_Function,
                     "EXTSENSE": self.Extsense}

        # Configurations to tests
        AvailableConfigurations = [
            key for key in configuration.keys() if key in map_tests.keys()]
        # Only tests in the map_tests will be tested
        # If the test is not int map_tests it is skipped
        SkippedTests = [key for key in configuration.keys()
                        if key not in map_tests.keys()]
        log(f"**** TESTING {AvailableConfigurations}")
        log(f"**** SKIPPING {SkippedTests}")
        TrueParameters = {}
        for parameter_to_test in AvailableConfigurations:
            test_function = map_tests[parameter_to_test]
            ActualValue = test_function()
            TrueParameters[parameter_to_test] = ActualValue
            time.sleep(2)
        return TrueParameters

    def Generate_Function(self):
        # Verificacion del instrumento
        # 1.000000000,V,0.00000000\n
        response = self.device.inst.query("OUT?").replace("\n", "").split(",")
        # ["1.000000000","V","0.000000000"]
        translator = {"A": "I", "V": "V", "OHM": "RES"}
        amplitude = float(response[0])
        magnitude = translator[response[1]]
        frequency = float(response[2])

        if magnitude == "RES":
            ActualFunction = self.FUNCTION[magnitude]
            return ActualFunction

        if frequency == 0:
            ActualFunction = self.FUNCTION["DC"+magnitude]
        else:
            ActualFunction = self.FUNCTION["AC"+magnitude]
        return ActualFunction

    def Amplitude_P1(self):
        actual_primary_amplitude = self.device.inst.query("OUT?").split(",")[0]
        actual_primary_amplitude = float(actual_primary_amplitude)
        return actual_primary_amplitude

    def Frequency(self):
        actual_Frequency = float(self.device.inst.query(
            "OUT?").split(',')[-1].replace("\n", ""))
        return actual_Frequency

    def Extsense(self):
        ISR_register = self.device.inst.query("ISR?").replace("\n", "")
        ISR_register = int(ISR_register)

        EXSENSE = (ISR_register >> 2) & 0x1

        if EXSENSE == 1:
            exsense = "ON"
        else:
            exsense = "OFF"

        return exsense

    def Zcomp(self):
        # 4 Hilos
        #	- EXSENSE ON
        #   - 2WIRE COMP OFF
        # 2 Hilos
        #	- EXSENSE OFF
        #	- 2WIRE COMP ON
        # Sin compensacion
        #	- EXSENSE OFF
        #	- 2WIRE COMP OFF

        ISR_register = self.device.inst.query("ISR?").replace("\n", "")
        ISR_register = int(ISR_register)

        EXSENSE = (ISR_register >> 2) & 0x1
        RCOMP = (ISR_register >> 4) & 0x1

        if (EXSENSE == 1) and (RCOMP == 0):
            actual_Zcomp = 4
        elif (EXSENSE == 0) and (RCOMP == 1):
            actual_Zcomp = 2
        else:
            actual_Zcomp = 0
        return actual_Zcomp


# Start Multimeter and test enviroment
Instrument = FLUKE_5720A('GPIB0::0::INSTR', simulation=SIMULATION)
ConfigReader = CalibratorConfiguration()
# Assign device to TEST
ConfigReader.device = Instrument

##############################################################################################
####################################### TESTS BEGINING #######################################
##############################################################################################


class DC_Tests(unittest.TestCase):

    def test_00(self):
        # Configuration: 100 mV, 7 V @ 0 HZ
        GENERATE_FUNCTION = "DCV"
        AMPLITUDE_P1 = 0.1
        EXTSENSE = "OFF"
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "EXTSENSE": EXTSENSE}

        Instrument.set_DCV(AMPLITUDE_P1, EXTSENSE)
        # Test Parameters
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["EXTSENSE"],
                         ConfigParameters["EXTSENSE"])

    def test_01(self):
        # Configuration: 1 V, 0 V @ 0 HZ
        GENERATE_FUNCTION = "DCV"
        AMPLITUDE_P1 = 1
        EXTSENSE = "ON"
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "EXTSENSE": EXTSENSE}

        Instrument.set_DCV(AMPLITUDE_P1, EXTSENSE)
        # Test Parameters
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["EXTSENSE"],
                         ConfigParameters["EXTSENSE"])

    def test_02(self):
        # Configuration: 100 V, 1 V @ 0 HZ
        GENERATE_FUNCTION = "DCV"
        AMPLITUDE_P1 = 100
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION}

        Instrument.set_DCV(AMPLITUDE_P1)
        # Test Parameters
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])

    def test_03(self):

        # Configuration: 100 mV, 1 V @ 60 HZ
        GENERATE_FUNCTION = "ACV"
        AMPLITUDE_P1 = 0.1
        AMPLITUDE_P2 = 1
        FREQUENCY = 60

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_04(self):
        # Configuration: 100 V @ 60 HZ
        GENERATE_FUNCTION = "ACV"
        AMPLITUDE_P1 = 10
        FREQUENCY = 60

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_05(self):

        # Configuration: 100 V, 7 V @ 60 HZ
        GENERATE_FUNCTION = "ACV"
        AMPLITUDE_P1 = 100
        FREQUENCY = 60

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_06(self):

        # Configuration: 100 mV, 1 V @ 1000 HZ
        GENERATE_FUNCTION = "ACV"
        AMPLITUDE_P1 = 0.1
        FREQUENCY = 1000

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_07(self):

        # Configuration: 10 V @ 1000 HZ
        GENERATE_FUNCTION = "ACV"
        AMPLITUDE_P1 = 10
        FREQUENCY = 1000

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_08(self):

        # Configuration: 100 V, 5 V @ 1000 HZ
        GENERATE_FUNCTION = "ACV"
        AMPLITUDE_P1 = 100
        AMPLITUDE_P2 = 5
        FREQUENCY = 1000

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_09(self):

        # Configuration: 0.1 mA @ 0 HZ
        GENERATE_FUNCTION = "DCI"
        AMPLITUDE_P1 = 0.1

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION}

        Instrument.set_DCI(AMPLITUDE_P1)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])

    def test_10(self):

        # Configuration: 1 A @ 0 HZ
        GENERATE_FUNCTION = "DCI"
        AMPLITUDE_P1 = 1

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION}

        Instrument.set_DCI(AMPLITUDE_P1)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])

    def test_11(self):

        # Configuration: 10 A @ 0 HZ
        GENERATE_FUNCTION = "DCI"
        AMPLITUDE_P1 = 2

        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION}

        Instrument.set_DCI(AMPLITUDE_P1)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])

    def test_12(self):

        # Configuration: 0.1 mA @ 60 HZ
        GENERATE_FUNCTION = "ACI"
        AMPLITUDE_P1 = 0.1
        FREQUENCY = 60
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACI(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_13(self):

        # Configuration: 1 A @ 0 HZ
        GENERATE_FUNCTION = "ACI"
        AMPLITUDE_P1 = 1
        FREQUENCY = 60
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACI(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_14(self):

        # Configuration: 2 A @ 0 HZ
        GENERATE_FUNCTION = "ACI"
        AMPLITUDE_P1 = 2
        FREQUENCY = 60
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "FREQUENCY": FREQUENCY}

        Instrument.set_ACI(AMPLITUDE_P1, FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(
            TrueParameters["FREQUENCY"], ConfigParameters["FREQUENCY"])

    def test_15(self):

        # Configuration: 10 OHM WIRE2
        GENERATE_FUNCTION = "RES"
        AMPLITUDE_P1 = 10
        ZCOMP = 2
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "ZCOMP": ZCOMP}

        Instrument.set_OHM(AMPLITUDE_P1, ZCOMP)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertAlmostEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"], 1)
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["ZCOMP"], ConfigParameters["ZCOMP"])

    def test_16(self):

        # Configuration: 100 OHM WIRE4
        GENERATE_FUNCTION = "RES"
        AMPLITUDE_P1 = 100
        ZCOMP = 4
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "ZCOMP": ZCOMP}

        Instrument.set_OHM(AMPLITUDE_P1, ZCOMP)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertAlmostEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"], 1)
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["ZCOMP"], ConfigParameters["ZCOMP"])

    def test_17(self):

        # Configuration: 100 OHM
        GENERATE_FUNCTION = "RES"
        AMPLITUDE_P1 = 100
        ZCOMP = 0
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "ZCOMP": ZCOMP}

        Instrument.set_OHM(AMPLITUDE_P1, ZCOMP)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertAlmostEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"], 1)
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["ZCOMP"], ConfigParameters["ZCOMP"])

    def test_18(self):

        # Configuration: 10 OHM WIRE2
        GENERATE_FUNCTION = "RES"
        AMPLITUDE_P1 = 10
        ZCOMP = 2
        ConfigParameters = {"AMPLITUDE_P1": AMPLITUDE_P1,
                            "GENERATE_FUNCTION": GENERATE_FUNCTION,
                            "ZCOMP": ZCOMP}

        Instrument.set_OHM(AMPLITUDE_P1, ZCOMP)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertAlmostEqual(
            TrueParameters["AMPLITUDE_P1"], ConfigParameters["AMPLITUDE_P1"], 1)
        self.assertEqual(
            TrueParameters["GENERATE_FUNCTION"], ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["ZCOMP"], ConfigParameters["ZCOMP"])


if __name__ == "__main__":
    unittest.main()
