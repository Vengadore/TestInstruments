import unittest
import sys
sys.path.append("../../../Generators")
from cal5XXXA import FLUKE_5500A 

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
        map_tests = {"AMPLITUDE_P1":self.Amplitude_P1,
                     "AMPLITUDE_P2":self.Amplitude_P2,
                     "FREQUENCY":self.Frequency,
                     "ZCOMP":self.Zcomp}
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

    def Amplitude_P1(self,expected:float):
        actual_primary_amplitude = self.device.inst.query("OUT?").split(",")[0]
        actual_primary_amplitude = float(actual_primary_amplitude)
        self.assertEqual(expected,actual_primary_amplitude,"Error in PRIMARY AMPLITUDE configuration")
        return 0

    def Amplitude_P2(self,expected:float):
        actual_second_amplitude = self.device.inst.query("OUT?").split(",")[2]
        actual_second_amplitude = float(actual_second_amplitude)
        self.assertEqual(expected,actual_second_amplitude,"Error in SECOND AMPLITUDE configuration")
        return 0
    
    def Frequency(self,expected:float):
        actual_Frequency = float(self.device.inst.query("OUT?").split(',')[-1].replace("\n",""))
        self.assertEqual(expected,actual_Frequency,"Error in FREQUENCY configuration")
        return 0

    def Zcomp(self,expected:float):
        actual_Zcomp = float(self.device.inst.query("OUT?").split(',')[-1].replace("\n",""))
        self.assertEqual(expected,actual_Zcomp,"Error in ZCOMP configuration")
        return 0


## Start Multimeter and test enviroment
Instrument = FLUKE_5500A(bus_connection='GPIB0::4::INSTR',simulation=SIMULATION)
TEST = ConfigurationTest()
# Assign device to TEST
TEST.device = Instrument

##############################################################################################
####################################### TESTS BEGINING #######################################
##############################################################################################

###################
##### TEST 00 #####
###################  

# Configuration: 100 mV, 7 V @ 0 HZ
AMPLITUDE_P1             = 0.1
AMPLITUDE_P2             = 7
ConfigParameters = {"AMPLITUDE_P1"           :AMPLITUDE_P1,
                    "AMPLITUDE_P2"           :AMPLITUDE_P2} 

Instrument.set_DCV(AMPLITUDE_P1,AMPLITUDE_P2)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 01 #####
###################  

# Configuration: 1 V, 0 V @ 0 HZ
AMPLITUDE_P1             = 1
AMPLITUDE_P2             = 0
ConfigParameters = {"AMPLITUDE_P1"           :AMPLITUDE_P1} 
                    
Instrument.set_DCV(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 02 #####
###################  

# Configuration: 100 V, 1 V @ 0 HZ
AMPLITUDE_P1             = 100
AMPLITUDE_P2             = 1
ConfigParameters = {"AMPLITUDE_P1"           :AMPLITUDE_P1,
                    "AMPLITUDE_P2"           :AMPLITUDE_P2} 

Instrument.set_DCV(AMPLITUDE_P1,AMPLITUDE_P2)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 03 #####
###################  

# Configuration: 100 mV, 1 V @ 60 HZ
AMPLITUDE_P1     = 0.1
AMPLITUDE_P2     = 1
FREQUENCY        = 60

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY, 
                    "AMPLITUDE_P2"    :AMPLITUDE_P2}

Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY,AMPLITUDE_P2)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 04 #####
###################  

# Configuration: 100 V @ 60 HZ
AMPLITUDE_P1     = 10
AMPLITUDE_P2     = 1
FREQUENCY        = 60

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY}

Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 05 #####
###################  

# Configuration: 100 V, 7 V @ 60 HZ
AMPLITUDE_P1     = 100
AMPLITUDE_P2     = 5
FREQUENCY        = 60

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY, 
                    "AMPLITUDE_P2"    :AMPLITUDE_P2}

Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY,AMPLITUDE_P2)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 06 #####
###################  

# Configuration: 100 mV, 1 V @ 1000 HZ
AMPLITUDE_P1     = 0.1
AMPLITUDE_P2     = 1
FREQUENCY        = 1000

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY, 
                    "AMPLITUDE_P2"    :AMPLITUDE_P2}

Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY,AMPLITUDE_P2)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 07 #####
###################  

# Configuration: 10 V @ 1000 HZ
AMPLITUDE_P1     = 10
AMPLITUDE_P2     = 1
FREQUENCY        = 1000

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY}

Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 08 #####
###################  

# Configuration: 100 V, 5 V @ 1000 HZ
AMPLITUDE_P1     = 100
AMPLITUDE_P2     = 5
FREQUENCY        = 1000

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY, 
                    "AMPLITUDE_P2"    :AMPLITUDE_P2}

Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY,AMPLITUDE_P2)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 08 #####
###################  

# Configuration: 100 V, 5 V @ 1000 HZ
AMPLITUDE_P1     = 100
AMPLITUDE_P2     = 5
FREQUENCY        = 1000

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY, 
                    "AMPLITUDE_P2"    :AMPLITUDE_P2}

Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY,AMPLITUDE_P2)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 09 #####
###################  

# Configuration: 0.1 mA @ 0 HZ
AMPLITUDE_P1     = 0.1

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1}

Instrument.set_DCI(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 10 #####
###################  

# Configuration: 1 A @ 0 HZ
AMPLITUDE_P1     = 1

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1}

Instrument.set_DCI(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 11 #####
###################  

# Configuration: 10 A @ 0 HZ
AMPLITUDE_P1     = 10

ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1}

Instrument.set_DCI(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 12 #####
###################  

# Configuration: 0.1 mA @ 60 HZ
AMPLITUDE_P1     = 0.1
FREQUENCY        = 60
ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY}

Instrument.set_ACI(AMPLITUDE_P1,FREQUENCY)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 13 #####
###################  

# Configuration: 1 A @ 0 HZ
AMPLITUDE_P1     = 1
FREQUENCY        = 60
ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY}

Instrument.set_ACI(AMPLITUDE_P1,FREQUENCY)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 14 #####
###################  

# Configuration: 10 A @ 0 HZ
AMPLITUDE_P1     = 10
FREQUENCY        = 60
ConfigParameters = {"AMPLITUDE_P1"    :AMPLITUDE_P1,
                    "FREQUENCY"       :FREQUENCY}

Instrument.set_ACI(AMPLITUDE_P1,FREQUENCY)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 15 #####
###################  

# Configuration: 10 OHM 
AMPLITUDE_P1     = 10
ZCOMP            = 0
ConfigParameters = {"AMPLITUDE_P1" :AMPLITUDE_P1}

Instrument.set_OHM(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 16 #####
###################  

# Configuration: 100 OHM
AMPLITUDE_P1     = 100
ZCOMP            = 4
ConfigParameters = {"AMPLITUDE_P1" :AMPLITUDE_P1}

Instrument.set_OHM(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 17 #####
###################  

# Configuration: 100 OHM
AMPLITUDE_P1     = 15
ZCOMP            = 2
ConfigParameters = {"AMPLITUDE_P1" :AMPLITUDE_P1}

Instrument.set_OHM(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 18 #####
###################  

# Configuration: 1 uF
AMPLITUDE_P1     =  0.00000001
ZCOMP            = 2
ConfigParameters = {"AMPLITUDE_P1" :AMPLITUDE_P1}

Instrument.set_CAP(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 19 #####
###################  

# Configuration: 1 uF
AMPLITUDE_P1     =  0.000001
ZCOMP            = 2
ConfigParameters = {"AMPLITUDE_P1" :AMPLITUDE_P1}

Instrument.set_CAP(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

###################
##### TEST 20 #####
###################  

# Configuration: 1 uF
AMPLITUDE_P1     =  0.0001
ZCOMP            = 2
ConfigParameters = {"AMPLITUDE_P1" :AMPLITUDE_P1}

Instrument.set_CAP(AMPLITUDE_P1)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)

