from Indicators.KeysightDMM import Keysight_3458A
import unittest
import time

# Test parameters
SIMULATION = False
LOGS = True


def log(message):
    if LOGS:
        print(message)


class ConfigurationTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.setup()

    def setup(self):
        self.device = Keysight_3458A(bus_connection='GPIB0::23::INSTR',
                                     simulation=SIMULATION)
        # Constats for test
        self.FUNCTION = {1: "DCV", 2: "ACV", 3: "ACDCV", 4: "OHM",
                         5: "OHMF", 6: "DCI", 7: "ACI", 8: "ACDCI",
                         9: "FREQ", 10: "PER", 11: "DSAC", 12: "DSDC",
                         13: "SSAC", 14: "SSDC"}
    
    def close_Conection(self):
        self.device.inst.close()

    def run_configuration(self, configuration: dict):
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
            time.sleep(5)
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

    def test_configuration_DCV_10V(self):
        MEASUREMENT_FUNCTION = "DCV"
        MEASUREMENT_RANGE = 10
        NPLC = 100
        NDIG = 8
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE,
                            "NPLC": NPLC,
                            "NDIG": NDIG}
        self.device.DCV(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_DCV_10V_NPLC_0_1(self):
        MEASUREMENT_FUNCTION = "DCV"
        MEASUREMENT_RANGE = 10
        NPLC = 100
        NDIG = 8
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE,
                            "NPLC": NPLC,
                            "NDIG": NDIG}
        self.device.DCV(MEASUREMENT_RANGE)
        self.device.SET_NPLC(100)
        self.run_configuration(ConfigParameters)

    def test_configuration_DCV_100V(self):
        MEASUREMENT_FUNCTION = "DCV"
        MEASUREMENT_RANGE = 100
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCV(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_DCV_100mV(self):
        MEASUREMENT_FUNCTION = "DCV"
        MEASUREMENT_RANGE = 0.1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCV(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_ACVSYNC_100mv(self):
        MEASUREMENT_FUNCTION = "ACV"
        MEASUREMENT_RANGE = 0.1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACVSYNC(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_OHMF_1kOhm_string(self):
        MEASUREMENT_FUNCTION = "OHMF"
        MEASUREMENT_RANGE = 1000
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.OHM("OHMF", "1 K")
        self.run_configuration(ConfigParameters)

    def test_confugration_OMHG_1kOhm_float(self):
        MEASUREMENT_FUNCTION = "OHMF"
        MEASUREMENT_RANGE = 1000
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.OHM("OHMF", MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_OHMF_100kOhm_string(self):
        MEASUREMENT_FUNCTION = "OHMF"
        MEASUREMENT_RANGE = 100000
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.OHM("OHMF", "100 K")
        self.run_configuration(ConfigParameters)

    def test_configuration_OHMF_100kOhm_float(self):
        MEASUREMENT_FUNCTION = "OHMF"
        MEASUREMENT_RANGE = 100000
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.OHM("OHMF", MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_OHM_100kOhm_string(self):
        MEASUREMENT_FUNCTION = "OHM"
        MEASUREMENT_RANGE = 100000
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.OHM("OHM", "100 K")
        self.run_configuration(ConfigParameters)

    def test_configuration_OHM_100kOhm_float(self):
        MEASUREMENT_FUNCTION = "OHM"
        MEASUREMENT_RANGE = 100000
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.OHM("OHM", MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_DCI_1mA_string(self):
        MEASUREMENT_FUNCTION = "DCI"
        MEASUREMENT_RANGE = 0.001
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCI("1 m")
        self.run_configuration(ConfigParameters)

    def test_configuration_DCI_1mA_float(self):
        MEASUREMENT_FUNCTION = "DCI"
        MEASUREMENT_RANGE = 0.001
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCI(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_DCI_10mA_string(self):
        MEASUREMENT_FUNCTION = "DCI"
        MEASUREMENT_RANGE = 0.01
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCI("10 m")
        self.run_configuration(ConfigParameters)

    def test_configuration_DCI_10mA_float(self):
        MEASUREMENT_FUNCTION = "DCI"
        MEASUREMENT_RANGE = 0.01
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCI(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_DCI_100mA_string(self):
        MEASUREMENT_FUNCTION = "DCI"
        MEASUREMENT_RANGE = 0.1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCI("100 m")
        self.run_configuration(ConfigParameters)

    def test_configuration_DCI_100mA_float(self):
        MEASUREMENT_FUNCTION = "DCI"
        MEASUREMENT_RANGE = 0.1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCI(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_DCI_1A_string(self):
        MEASUREMENT_FUNCTION = "DCI"
        MEASUREMENT_RANGE = 1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCI("1 A")
        self.run_configuration(ConfigParameters)

    def test_configuration_DCI_1A_float(self):
        MEASUREMENT_FUNCTION = "DCI"
        MEASUREMENT_RANGE = 1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.DCI(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_ACI_1mA_string(self):
        MEASUREMENT_FUNCTION = "ACI"
        MEASUREMENT_RANGE = 0.001
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACI("1 m")
        self.run_configuration(ConfigParameters)

    def test_configuration_ACI_1mA_float(self):
        MEASUREMENT_FUNCTION = "ACI"
        MEASUREMENT_RANGE = 0.001
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACI(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_ACI_10mA_string(self):
        MEASUREMENT_FUNCTION = "ACI"
        MEASUREMENT_RANGE = 0.01
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACI("10 m")
        self.run_configuration(ConfigParameters)

    def test_configuration_ACI_10mA_float(self):
        MEASUREMENT_FUNCTION = "ACI"
        MEASUREMENT_RANGE = 0.01
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACI(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_ACI_100mA_string(self):
        MEASUREMENT_FUNCTION = "ACI"
        MEASUREMENT_RANGE = 0.1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACI("100 m")
        self.run_configuration(ConfigParameters)

    def test_configuration_ACI_100mA_float(self):
        MEASUREMENT_FUNCTION = "ACI"
        MEASUREMENT_RANGE = 0.1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACI(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)

    def test_configuration_ACI_1A_string(self):
        MEASUREMENT_FUNCTION = "ACI"
        MEASUREMENT_RANGE = 1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACI("1 A")
        self.run_configuration(ConfigParameters)

    def test_configuration_ACI_1A_float(self):
        MEASUREMENT_FUNCTION = "ACI"
        MEASUREMENT_RANGE = 1
        ConfigParameters = {"MEASUREMENT_FUNCTION": MEASUREMENT_FUNCTION,
                            "MEASUREMENT_RANGE": MEASUREMENT_RANGE}
        self.device.ACI(MEASUREMENT_RANGE)
        self.run_configuration(ConfigParameters)


if __name__ == '__main__':
    unittest.main()
