from Indicators.KeysightDMM import Keysight_3458A
import unittest

# Test parameters
SIMULATION = False
LOGS = True

# Test functions


def log(message):
    if LOGS:
        print(message)


class ConfigurationTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.device = object
    # Constats for test
    FUNCTION = {1: "DCV", 2: "ACV", 3: "ACDCV", 4: "OHM",
                5: "OHMF", 6: "DCI", 7: "ACI", 8: "ACDCI",
                9: "FREQ", 10: "PER", 11: "DSAC", 12: "DSDC",
                13: "SSAC", 14: "SSDC"}

    # Available tests
#   MEASUREMENT_FUNCTION
#   MEASUREMENT_RANGE
#   NPLC
#   RES
#   NDIG

    def test_configuration(self, configuration: dict):
        map_tests = {"MEASUREMENT_FUNCTION": self.Measurement_function,
                     "MEASUREMENT_RANGE": self.Measurement_range,
                     "NPLC": self.NPLC,
                     "RES": self.RES,
                     "NDIG": self.NDIG}
        # Configurations to tests
        AvailableConfigurations = [key for key in configuration.keys(
        ) if key in map_tests.keys()]  # Only tests in the map_tests will be tested
        # If the test is not int map_tests it is skipped
        SkippedTests = [key for key in configuration.keys()
                        if key not in map_tests.keys()]
        log(f"**** TESTING {AvailableConfigurations}")
        log(f"**** SKIPPING {SkippedTests}")
        for parameter_to_test in AvailableConfigurations:
            test_function = map_tests[parameter_to_test]
            expectedValue = configuration[parameter_to_test]
            # Test
            log(f"Testing parameter {parameter_to_test}:{expectedValue}")
            test_function(expectedValue)
        return 0

    def Measurement_function(self, expected: str):
        actual_measurement_function = self.FUNCTION[int(
            self.device.inst.query("FUNC?").split(",")[0])]
        self.assertEqual(expected, actual_measurement_function,
                         "Error in MEASUREMENT FUNCTION configuration")
        return 0

    def Measurement_range(self, expected: float):
        actual_measurement_range = float(
            self.device.inst.query("FUNC?").split(" ")[1])
        self.assertEqual(expected, actual_measurement_range,
                         "Error in MEASUREMENT RANGE configuration")
        return 0

    def NPLC(self, expected: float):
        actual_NPLC = float(self.device.inst.query("NPLC?"))
        self.assertEqual(expected, actual_NPLC, "Error in NPLC configuration")
        return 0

    def RES(self, expected: float):
        actual_RES = float(self.device.inst.query("RES?"))
        self.assertEqual(expected, actual_RES, "Error in RES configuration")
        return 0

    def NDIG(self, expected: float):
        actual_RES = float(self.device.inst.query("NDIG?"))
        self.assertEqual(expected, actual_RES, "Error in NDIG configuration")
        return 0


# Start Multimeter and test enviroment
Instrument = Keysight_3458A(
    bus_connection='GPIB0::14::INSTR', simulation=SIMULATION)
TEST = ConfigurationTest()
# Assign device to TEST
TEST.device = Instrument

##############################################################################################
####################################### TESTS BEGINING #######################################
##############################################################################################

###################
##### TEST 00 #####
###################
# Configuration: DCV @ 10 V
MEASUREMENT_FUNCTION = "DCV"
MEASUREMENT_RANGE = 10
NPLC = 100
NDIG = 8
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE,
                    "NPLC": NPLC,
                    "NDIG": NDIG}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 00b ####
###################
# Configuration: DCV @ 10 V, NPLC=0.1
MEASUREMENT_FUNCTION = "DCV"
MEASUREMENT_RANGE = 10
NPLC = 100
NDIG = 8
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE,
                    "NPLC": NPLC,
                    "NDIG": NDIG}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
Instrument.SET_NPLC(100)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 01 #####
###################
# Configuration: DCV @ 100 V
MEASUREMENT_FUNCTION = "DCV"
MEASUREMENT_RANGE = 100
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 02 #####
###################
# Configuration: DCV @ 100 mV
MEASUREMENT_FUNCTION = "DCV"
MEASUREMENT_RANGE = 0.1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 03 #####
###################
# Configuration: ACVSYNC @ 100 mV
MEASUREMENT_FUNCTION = "ACV"
MEASUREMENT_RANGE = 0.1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACVSYNC(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 04 #####
###################
# Configuration: OHMF @ 1 KOhm (Medición de resistencia a 4 hilos, alcance de 100 Ohms)
MEASUREMENT_FUNCTION = "OHMF"
MEASUREMENT_RANGE = 1000
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.OHM("OHMF", "1 K")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 05 #####
###################
# Configuration: OHMF @ 1 KOhm (Medición de resistencia a 4 hilos, alcance de 100 Ohms)
MEASUREMENT_FUNCTION = "OHMF"
MEASUREMENT_RANGE = 1000
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.OHM("OHMF", 1000)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 06 #####
###################
# Configuration: OHMF @ 100 KOhm (Medición de resistencia a 4 hilos, alcance de 100 kOhms)
MEASUREMENT_FUNCTION = "OHMF"
MEASUREMENT_RANGE = 100000
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.OHM("OHMF", "100 K")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 07 #####
###################
# Configuration: OHMF @ 100 KOhm (Medición de resistencia a 4 hilos, alcance de 100 kOhms)
MEASUREMENT_FUNCTION = "OHMF"
MEASUREMENT_RANGE = 100000
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.OHM("OHMF", 100000)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 08 #####
###################
# Configuration: OHM @ 100 KOhm (Medición de resistencia a 2 hilos, alcance de 100 KOhms)
MEASUREMENT_FUNCTION = "OHM"
MEASUREMENT_RANGE = 100000
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.OHM("OHM", "100 K")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 09 #####
###################
# Configuration: OHM @ 100 KOhm (Medición de resistencia a 2 hilos, alcance de 100 KOhms)
MEASUREMENT_FUNCTION = "OHM"
MEASUREMENT_RANGE = 100000
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.OHM("OHM", 100000)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 10 #####
###################
# Configuration: DCI @ 1mA (Medición de corriente directa, alcance de 1mA)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE = 0.001
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI("1 m")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 11 #####
###################
# Configuration: DCI @ 1mA (Medición de corriente directa, alcance de 1mA)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE = 0.001
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI(0.001)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 12 #####
###################
# Configuration: DCI @ 10mA (Medición de corriente directa, alcance de 10mA)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE = 0.01
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI("10 m")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 13 #####
###################
# Configuration: DCI @ 10mA (Medición de corriente directa, alcance de 10mA)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE = 0.01
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI(0.01)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 14 #####
###################
# Configuration: DCI @ 100mA (Medición de corriente directa, alcance de 100mA)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE = 0.1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI("100 m")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 15 #####
###################
# Configuration: DCI @ 100mA (Medición de corriente directa, alcance de 100mA)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE = 0.1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI(0.1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 16 #####
###################
# Configuration: DCI @ 1A (Medición de corriente directa, alcance de 1A)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE = 1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI("1 A")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 17 #####
###################
# Configuration: DCI @ 1A (Medición de corriente directa, alcance de 1A)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE = 1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI(1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 18 #####
###################
# Configuration: ACI @ 1mA (Medición de corriente alterna, alcance de 1mA)
MEASUREMENT_FUNCTION = "ACI"
MEASUREMENT_RANGE = 0.001
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACI("1 m")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 19 #####
###################
# Configuration: ACI @ 1mA (Medición de corriente alterna, alcance de 1mA)
MEASUREMENT_FUNCTION = "ACI"
MEASUREMENT_RANGE = 0.001
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACI(0.001)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 20 #####
###################
# Configuration: ACI @ 10mA (Medición de corriente alterna, alcance de 10mA)
MEASUREMENT_FUNCTION = "ACI"
MEASUREMENT_RANGE = 0.01
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACI("10 m")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 21 #####
###################
# Configuration: ACI @ 10mA (Medición de corriente alterna, alcance de 10mA)
MEASUREMENT_FUNCTION = "ACI"
MEASUREMENT_RANGE = 0.01
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACI(0.01)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 22 #####
###################
# Configuration: ACI @ 100mA (Medición de corriente alterna, alcance de 100mA)
MEASUREMENT_FUNCTION = "ACI"
MEASUREMENT_RANGE = 0.1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACI("100 m")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 23 #####
###################
# Configuration: ACI @ 100mA (Medición de corriente alterna, alcance de 100mA)
MEASUREMENT_FUNCTION = "ACI"
MEASUREMENT_RANGE = 0.1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACI(0.1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 24 #####
###################
# Configuration: ACI @ 1A (Medición de corriente alterna, alcance de 1A)
MEASUREMENT_FUNCTION = "ACI"
MEASUREMENT_RANGE = 1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACI("1 A")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 25 #####
###################
# Configuration: ACI @ 1A (Medición de corriente alterna, alcance de 1A)
MEASUREMENT_FUNCTION = "ACI"
MEASUREMENT_RANGE = 1
ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACI(1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


if __name__ == '__main__':
    unittest.main()
