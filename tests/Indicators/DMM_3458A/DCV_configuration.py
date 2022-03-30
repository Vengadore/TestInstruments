import unittest
import sys
sys.path.append("../../../Indicators")
from KeysightDMM import Keysight_3458A 

## Test parameters
SIMULATION = False
LOGS       = True

## Test functions
def log(message):
    if LOGS:
        print(message)

class ConfigurationTest(unittest.TestCase):
    ## Constats for test
    FUNCTION = {1:"DCV",2:"ACV",3:"ACDCV",4:"OHM",
                5:"OHMF",6:"DCI",7:"ACI",8:"ACDCI",
                9:"FREQ",10:"PER",11:"DSAC",12:"DSDC",
                13:"SSAC",14:"SSDC"}

    ## Available tests
#   MEASUREMENT_FUNCTION
#   MEASUREMENT_RANGE     
#   NPLC 
#   RES 
# 

    def test_configuration(self,configuration:dict):
        map_tests = {"MEASUREMENT_FUNCTION":self.Measurement_function,
                     "MEASUREMENT_RANGE":self.Measurement_range,
                     "NPLC":self.NPLC,
                     "RES":self.RES}
        # Configurations to tests
        AvailableConfigurations = [key for key in configuration.keys() if key in map_tests.keys()] # Only tests in the map_tests will be tested
        SkippedTests = [key for key in configuration.keys() if key not in map_tests.keys()]        # If the test is not int map_tests it is skipped
        log(f"**** TESTING {AvailableConfigurations}")
        log(f"**** SKIPPING {SkippedTests}")
        for parameter_to_test in AvailableConfigurations:
            test_function = map_tests[parameter_to_test]
            expectedValue = configuration[parameter_to_test]
            # Test
            log(f"Testing parameter {parameter_to_test}:{expectedValue}")
            test_function(expectedValue)
        return 0

    def Measurement_function(self,expected:str):
        actual_measurement_function = self.FUNCTION[int(self.device.inst.query("FUNC?").split(",")[0])]
        self.assertEqual(expected,actual_measurement_function,"Error in MEASUREMENT FUNCTION configuration")
        return 0
    
    def Measurement_range(self,expected:float):
        actual_measurement_range = float(self.device.inst.query("FUNC?").split(" ")[1])
        self.assertEqual(expected,actual_measurement_range,"Error in MEASUREMENT RANGE configuration")
        return 0

    def NPLC(self,expected:float):
        actual_NPLC = float(self.device.inst.query("NPLC?"))
        self.assertEqual(expected,actual_NPLC,"Error in NPLC configuration")
        return 0
    
    def RES(self,expected:float):
        actual_RES = float(self.device.inst.query("RES?"))
        self.assertEqual(expected,actual_RES,"Error in RES configuration")
        return 0


## Start Multimeter and test enviroment
Instrument = Keysight_3458A(bus_connection='GPIB0::23::INSTR',simulation=SIMULATION)
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
MEASUREMENT_RANGE    = 10
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 01 #####
###################
# Configuration: DCV @ 100 V
MEASUREMENT_FUNCTION = "DCV"
MEASUREMENT_RANGE    = 100
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 02 #####
###################
# Configuration: DCV @ 100 mV
MEASUREMENT_FUNCTION = "DCV"
MEASUREMENT_RANGE    = 0.1
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 03 #####
###################
# Configuration: ACVSYNC @ 100 mV
MEASUREMENT_FUNCTION = "ACV"
MEASUREMENT_RANGE    = 0.1
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.ACVSYNC(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

