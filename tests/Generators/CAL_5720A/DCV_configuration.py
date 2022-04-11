import unittest
import sys
sys.path.append("../../../Generators")
from cal5XXXA import Fluke_5720A 

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
#   AMPLITUDE_P     
#   MAGNITUDE_GENERATED_P        
#   RANGE_P
#   FREQUENCY               

    def test_configuration(self,configuration:dict):
        map_tests = {"AMPLITUDE_P":self.Amplitude_P,
                     "MAGNITUDE_GENERATED_P":self.Magnitude_P,
                     "RANGE":self.Range_P,
                     "FREQUENCY":self.Frequency}
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

    def Amplitude_P(self,expected:float):
        actual_primary_amplitude = self.device.inst.query("OUT?").split(",")[0]
        actual_primary_amplitude = float(actual_primary_amplitude)
        self.assertEqual(expected,actual_primary_amplitude,"Error in PRIMARY AMPLITUDE configuration")
        return 0
    
    def Magnitude_P(self,expected:str):
        actual_primary_magnitude = self.device.inst.query("OUT?").split(",")[1]
        self.assertEqual(expected,actual_primary_magnitude,"Error in PRIMARY MAGNITUDE configuration")
        return 0

    def Range_P(self,expected:str):
        actual_Range = self.device.inst.query("RANGE?").split(",")[0]
        self.assertEqual(expected,actual_Range,"Error in RANGE configuration")
        return 0
    
    def Frequency(self,expected:float):
        actual_Frequency = float(self.device.inst.query("OUT?").split(',')[-1].replace("\n",""))
        self.assertEqual(expected,actual_Frequency,"Error in FREQUENCY configuration")
        return 0

## Start Multimeter and test enviroment
Instrument = Fluke_5720A(bus_connection='GPIB0::4::INSTR',simulation=SIMULATION)
TEST = ConfigurationTest()
# Assign device to TEST
TEST.device = Instrument

##############################################################################################
####################################### TESTS BEGINING #######################################
##############################################################################################

###################
##### TEST 00 #####
###################

#   AMPLITUDE_P     
#   MAGNITUDE_GENERATED_P        
#   RANGE_P
#   FREQUENCY     

# Configuration: 10 V @ 0 HZ
AMPLITUDE_P             = 10
MAGNITUDE_GENERATED_P   = "V" 
FREQUENCY               = 0
ConfigParameters = {"AMPLITUDE_P"           :AMPLITUDE_P,
                    "MAGNITUDE_GENERATED_P" :MAGNITUDE_GENERATED_P,
                    "FREQUENCY"             :FREQUENCY}
# Sending configuration to instrument
# SET debe ser una función que reciba un parametro flotante llamado amplitud, un parametro en forma de cadena
# llamado magnitud, y un parametro en forma de flotante llamado frecuencia.
# SET debe ser capaz de setear el calibrador a la magnitud que se indique y frecuencia debe tener un valor por 
# default de None, lo que indicará que no se mandará el parametro de frecuencia.
# Instrument.SET(10,"V",frecuencia = None)
Instrument("OUT 10 V, 0 HZ")
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


#if __name__ == '__main__':
#    unittest.main()