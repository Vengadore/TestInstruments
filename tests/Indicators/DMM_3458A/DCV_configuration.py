from codecs import namereplace_errors
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
#   NDIG

    def test_configuration(self,configuration:dict):
        map_tests = {"MEASUREMENT_FUNCTION":self.Measurement_function,
                     "MEASUREMENT_RANGE":self.Measurement_range,
                     "NPLC":self.NPLC,
                     "RES":self.RES,
                     "NDIG":self.NDIG}
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

    def NDIG(self,expected:float):
        actual_RES = float(self.device.inst.query("NDIG?"))
        self.assertEqual(expected,actual_RES,"Error in NDIG configuration")
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
<<<<<<< HEAD
MEASUREMENT_RANGE    = 10 
=======
MEASUREMENT_RANGE    = 10
>>>>>>> a948caf524d1a6c2485b6ba3ba74089e62ed8728
NPLC                 = 100
NDIG                 = 8
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE,
                    "NPLC":NPLC,
                    "NDIG":NDIG}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 00b ####
###################
# Configuration: DCV @ 10 V, NPLC=0.1
MEASUREMENT_FUNCTION = "DCV"
MEASUREMENT_RANGE    = 10
<<<<<<< HEAD
NPLC                 = 100
=======
NPLC                 = 0.1
>>>>>>> a948caf524d1a6c2485b6ba3ba74089e62ed8728
NDIG                 = 8
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE,
                    "NPLC":NPLC,
                    "NDIG":NDIG}
# Sending configuration to instrument
Instrument.DCV(MEASUREMENT_RANGE)
<<<<<<< HEAD
Instrument.SET_NPLC(100)
=======
Instrument.SET_NPLC(0.1)
>>>>>>> a948caf524d1a6c2485b6ba3ba74089e62ed8728
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


###################
##### TEST 04 #####
###################
# Configuration: OHMF @ 1 KOhm (Medición de resistencia a 4 hilos, alcance de 100 Ohms)
MEASUREMENT_FUNCTION = "OHMF"
MEASUREMENT_RANGE    = 1000
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
<<<<<<< HEAD
Instrument.OHM("OHMF","1 K")
=======
Instrument.OHM("OHMF","1 KOHM")
>>>>>>> a948caf524d1a6c2485b6ba3ba74089e62ed8728
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 04 #####
###################
# Configuration: OHMF @ 1 KOhm (Medición de resistencia a 4 hilos, alcance de 100 Ohms)
MEASUREMENT_FUNCTION = "OHMF"
MEASUREMENT_RANGE    = 1000
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.OHM("OHMF",1000)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 05 #####
###################
# Configuration: OHMF @ 100 KOhm (Medición de resistencia a 4 hilos, alcance de 100 kOhms)
<<<<<<< HEAD
MEASUREMENT_FUNCTION = "OHMF"
=======
MEASUREMENT_FUNCTION = "OHM"
>>>>>>> a948caf524d1a6c2485b6ba3ba74089e62ed8728
MEASUREMENT_RANGE    = 100000
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
<<<<<<< HEAD
Instrument.OHM("OHMF","100 K")
=======
Instrument.OHM("OHMF","100 KOHM")
>>>>>>> a948caf524d1a6c2485b6ba3ba74089e62ed8728
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 06 #####
###################
# Configuration: OHMF @ 100 KOhm (Medición de resistencia a 4 hilos, alcance de 100 kOhms)
MEASUREMENT_FUNCTION = "OHMF"
MEASUREMENT_RANGE    = 100000
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.OHM("OHMF",100000)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)



###################
##### TEST 08 #####
###################
# Configuration: OHM @ 100 KOhm (Medición de resistencia a 2 hilos, alcance de 100 KOhms)





###################
##### TEST 09 #####
###################
# Configuration: OHM @ 100 KOhm (Medición de resistencia a 2 hilos, alcance de 100 KOhms)




###################
##### TEST 10 #####
###################
# Configuration: DCI @ 1mA (Medición de corriente directa, alcance de 1mA)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE    = 0.001
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
<<<<<<< HEAD
Instrument.DCI("1 m")
=======
Instrument.DCI("1 mA")
>>>>>>> a948caf524d1a6c2485b6ba3ba74089e62ed8728
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)


###################
##### TEST 11 #####
###################
# Configuration: DCI @ 1mA (Medición de corriente directa, alcance de 1mA)
MEASUREMENT_FUNCTION = "DCI"
MEASUREMENT_RANGE    = 0.001
ConfigParameters = {"MEASUREMENT_FUNCTION":MEASUREMENT_FUNCTION,
                    "MEASUREMENT_RANGE" : MEASUREMENT_RANGE}
# Sending configuration to instrument
Instrument.DCI(0.001)
# Checking for correct configuration
TEST.test_configuration(ConfigParameters)



###################
##### TEST 11 #####
###################
# Configuration: DCI @ 10mA (Medición de corriente directa, alcance de 10mA)




###################
##### TEST 12 #####
###################
# Configuration: DCI @ 100mA (Medición de corriente directa, alcance de 100mA)



###################
##### TEST 13 #####
###################
# Configuration: DCI @ 1A (Medición de corriente directa, alcance de 1A)




###################
##### TEST 14 #####
###################
# Configuration: ACI @ 1mA (Medición de corriente directa, alcance de 1mA)


###################
##### TEST 15 #####
###################
# Configuration: ACI @ 10mA (Medición de corriente directa, alcance de 10mA)



###################
##### TEST 16 #####
###################
# Configuration: ACI @ 100mA (Medición de corriente directa, alcance de 100mA)



###################
##### TEST 17 #####
###################
# Configuration: ACI @ 1A (Medición de corriente directa, alcance de 1A)



<<<<<<< HEAD
=======














>>>>>>> a948caf524d1a6c2485b6ba3ba74089e62ed8728
#if __name__ == '__main__':
#    unittest.main()