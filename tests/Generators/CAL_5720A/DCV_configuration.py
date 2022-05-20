from argparse import Action
import unittest
import sys
import time
sys.path.append("../../../Generators")
from cal5XXXA import FLUKE_5720A

## Test parameters
SIMULATION = False
LOGS       = True

## Test functions
def log(message):
    if LOGS:
        print(message)

class CalibratorConfiguration():
    ## Constats for test
    FUNCTION = {'DCV':"DCV",'ACV':"ACV",'DCI':"DCI",'ACI':"ACI",
                'RES':"RES",'CAP':"CAP",'RTD':"RTD",'TC_OUT':"TC_OUT",
                'DC_POWER':"DC_POWER",'AC_POWER':"AC_POWER",'DCV_DCV':"DCV_DCV",'ACV_ACV':"ACV_ACV",'TC_MEAS':"TC_MEAS"}

    ## Available tests
#   AMPLITUDE_P     
#   MAGNITUDE_GENERATED_P        
#   RANGE_P
#   FREQUENCY               

    def test_configuration(self,configuration:dict):
        map_tests = {"AMPLITUDE_P1":self.Amplitude_P1,
                     "FREQUENCY":self.Frequency,
                     "ZCOMP":self.Zcomp,
                     "GENERATE_FUNCTION":self.Generate_Function}

        # Configurations to tests
        AvailableConfigurations = [key for key in configuration.keys() if key in map_tests.keys()] # Only tests in the map_tests will be tested
        SkippedTests = [key for key in configuration.keys() if key not in map_tests.keys()]        # If the test is not int map_tests it is skipped
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
        response = self.device.inst.query("OUT?").replace("\n","").split(",")
        # ["1.000000000","V","0.000000000"]
        translator = {"A":"I","V":"V","OHM":"RES"}
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
        actual_Frequency = float(self.device.inst.query("OUT?").split(',')[-1].replace("\n",""))
        return actual_Frequency

    def Zcomp(self):
        #4 Hilos
        #	- EXSENSE ON
        #   - 2WIRE COMP OFF
        #2 Hilos
        #	- EXSENSE OFF
        #	- 2WIRE COMP ON
        #Sin compensacion
        #	- EXSENSE OFF
        #	- 2WIRE COMP OFF

        ISR_register = self.device.inst.query("ISR?").replace("\n","")
        ISR_register = int(ISR_register)

        EXSENSE = (ISR_register>>2) & 0x1
        RCOMP   = (ISR_register>>4) & 0x1

        if (EXSENSE == 1) and (RCOMP == 0):
            actual_Zcomp = 4
        elif (EXSENSE == 0) and (RCOMP == 1):
            actual_Zcomp = 2
        else:
            actual_Zcomp = 0
        return actual_Zcomp

## Start Multimeter and test enviroment
Instrument = FLUKE_5720A()
ConfigReader = CalibratorConfiguration()
# Assign device to TEST
ConfigReader.device = Instrument

##############################################################################################
####################################### TESTS BEGINING #######################################
##############################################################################################

class DC_Tests(unittest.TestCase):

    def test_00(self):
        # Configuration: 100 mV, 7 V @ 0 HZ
        GENERATE_FUNCTION        = "DCV"
        AMPLITUDE_P1             = 0.1
        ConfigParameters = {"AMPLITUDE_P1"           :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"      :GENERATE_FUNCTION} 
        
        Instrument.set_DCV(AMPLITUDE_P1)
        ## Test Parameters
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])

    def test_01(self):
        # Configuration: 1 V, 0 V @ 0 HZ
        GENERATE_FUNCTION        = "DCV"
        AMPLITUDE_P1             = 1
        ConfigParameters = {"AMPLITUDE_P1"           :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"      :GENERATE_FUNCTION} 
        
        Instrument.set_DCV(AMPLITUDE_P1)
        ## Test Parameters
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])

    def test_02(self):
        # Configuration: 100 V, 1 V @ 0 HZ
        GENERATE_FUNCTION        = "DCV_DCV"
        AMPLITUDE_P1             = 100
        ConfigParameters = {"AMPLITUDE_P1"           :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"      :GENERATE_FUNCTION} 
        
        Instrument.set_DCV(AMPLITUDE_P1)
        ## Test Parameters
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])

    def test_03(self):

        # Configuration: 100 mV, 1 V @ 60 HZ
        GENERATE_FUNCTION   = "ACV"
        AMPLITUDE_P1        = 0.1
        AMPLITUDE_P2        = 1
        FREQUENCY           = 60

        ConfigParameters = {"AMPLITUDE_P1"       :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"  :GENERATE_FUNCTION,
                            "FREQUENCY"          :FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["FREQUENCY"]         ,ConfigParameters["FREQUENCY"])

    def test_04(self):
        # Configuration: 100 V @ 60 HZ
        GENERATE_FUNCTION   = "ACV"
        AMPLITUDE_P1        = 10
        FREQUENCY           = 60

        ConfigParameters = {"AMPLITUDE_P1"       :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"  :GENERATE_FUNCTION,
                            "FREQUENCY"          :FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["FREQUENCY"]         ,ConfigParameters["FREQUENCY"])

    def test_05(self): 

        # Configuration: 100 V, 7 V @ 60 HZ
        GENERATE_FUNCTION  = "ACV_ACV"
        AMPLITUDE_P1       = 100
        AMPLITUDE_P2       = 5
        FREQUENCY          = 60

        ConfigParameters = {"AMPLITUDE_P1"       :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"  :GENERATE_FUNCTION,
                            "FREQUENCY"          :FREQUENCY, 
                            "AMPLITUDE_P2"       :AMPLITUDE_P2}

        Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY,AMPLITUDE_P2)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["AMPLITUDE_P2"]      ,ConfigParameters["AMPLITUDE_P2"])
        self.assertEqual(TrueParameters["FREQUENCY"]         ,ConfigParameters["FREQUENCY"])

    def test_06(self): 

        # Configuration: 100 mV, 1 V @ 1000 HZ
        GENERATE_FUNCTION  = "ACV_ACV"
        AMPLITUDE_P1       = 0.1
        AMPLITUDE_P2       = 1
        FREQUENCY          = 1000

        ConfigParameters = {"AMPLITUDE_P1"       :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"  :GENERATE_FUNCTION,
                            "FREQUENCY"          :FREQUENCY, 
                            "AMPLITUDE_P2"       :AMPLITUDE_P2}

        Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY,AMPLITUDE_P2)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["AMPLITUDE_P2"]      ,ConfigParameters["AMPLITUDE_P2"])
        self.assertEqual(TrueParameters["FREQUENCY"]         ,ConfigParameters["FREQUENCY"])

    def test_07(self): 
        
        # Configuration: 10 V @ 1000 HZ
        GENERATE_FUNCTION  = "ACV"
        AMPLITUDE_P1       = 10
        FREQUENCY          = 1000

        ConfigParameters = {"AMPLITUDE_P1"       :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"  :GENERATE_FUNCTION,
                            "FREQUENCY"          :FREQUENCY}

        Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["FREQUENCY"]         ,ConfigParameters["FREQUENCY"])

    def test_08(self): 
        
        # Configuration: 100 V, 5 V @ 1000 HZ
        GENERATE_FUNCTION  = "ACV_ACV"
        AMPLITUDE_P1       = 100
        AMPLITUDE_P2       = 5
        FREQUENCY          = 1000

        ConfigParameters = {"AMPLITUDE_P1"       :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"  :GENERATE_FUNCTION,
                            "FREQUENCY"          :FREQUENCY, 
                            "AMPLITUDE_P2"       :AMPLITUDE_P2}

        Instrument.set_ACV(AMPLITUDE_P1,FREQUENCY,AMPLITUDE_P2)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])
        self.assertEqual(TrueParameters["AMPLITUDE_P2"]      ,ConfigParameters["AMPLITUDE_P2"])
        self.assertEqual(TrueParameters["FREQUENCY"]         ,ConfigParameters["FREQUENCY"])

    def test_09(self): 

        # Configuration: 0.1 mA @ 0 HZ
        GENERATE_FUNCTION  = "DCI"
        AMPLITUDE_P1       = 0.1

        ConfigParameters = {"AMPLITUDE_P1"       :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"  :GENERATE_FUNCTION}

        Instrument.set_DCI(AMPLITUDE_P1)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])

    def test_10(self): 

        # Configuration: 1 A @ 0 HZ
        GENERATE_FUNCTION  = "DCI"
        AMPLITUDE_P1       = 1

        ConfigParameters = {"AMPLITUDE_P1"       :AMPLITUDE_P1,
                            "GENERATE_FUNCTION"  :GENERATE_FUNCTION}

        Instrument.set_DCI(AMPLITUDE_P1)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])

    def test_11(self):
        
        # Configuration: 10 A @ 0 HZ
        GENERATE_FUNCTION  = "DCI"
        AMPLITUDE_P1       = 10

        ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
                            "GENERATE_FUNCTION" :GENERATE_FUNCTION}

        Instrument.set_DCI(AMPLITUDE_P1)
        # Checking for correct configuration
        TrueParameters = ConfigReader.test_configuration(ConfigParameters)
        self.assertEqual(TrueParameters["AMPLITUDE_P1"]      ,ConfigParameters["AMPLITUDE_P1"])
        self.assertEqual(TrueParameters["GENERATE_FUNCTION"] ,ConfigParameters["GENERATE_FUNCTION"])
    
####################
###### TEST 12 #####
####################  
#
## Configuration: 0.1 mA @ 60 HZ
#GENERATE_FUNCTION  = "ACI"
#AMPLITUDE_P1       = 0.1
#FREQUENCY          = 60
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "FREQUENCY"         :FREQUENCY}
#
#Instrument.set_ACI(AMPLITUDE_P1,FREQUENCY)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 13 #####
####################  
#
## Configuration: 1 A @ 0 HZ
#GENERATE_FUNCTION  = "ACI"
#AMPLITUDE_P1       = 1
#FREQUENCY          = 60
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "FREQUENCY"         :FREQUENCY}
#
#Instrument.set_ACI(AMPLITUDE_P1,FREQUENCY)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 14 #####
####################  
#
## Configuration: 10 A @ 0 HZ
#GENERATE_FUNCTION  = "ACI"
#AMPLITUDE_P1       = 10
#FREQUENCY          = 60
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "FREQUENCY"         :FREQUENCY}
#
#Instrument.set_ACI(AMPLITUDE_P1,FREQUENCY)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 15 #####
####################  
#
## Configuration: 10 OHM WIRE2
#GENERATE_FUNCTION  = "RES"
#AMPLITUDE_P1       = 10
#ZCOMP              = 2
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP}
#
#Instrument.set_OHM(AMPLITUDE_P1,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 16 #####
####################  
#
## Configuration: 100 OHM WIRE4
#GENERATE_FUNCTION  = "RES"
#AMPLITUDE_P1     = 100
#ZCOMP            = 4
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP}
#
#Instrument.set_OHM(AMPLITUDE_P1,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 17 #####
####################  
#
## Configuration: 100 OHM NONE
#GENERATE_FUNCTION  = "RES"
#AMPLITUDE_P1     = 15
#ZCOMP            = 0
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP}
#
#Instrument.set_OHM(AMPLITUDE_P1,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 18 #####
####################  
#
## Configuration: 100 nF
#GENERATE_FUNCTION  = "CAP"
#AMPLITUDE_P1     =  0.0000001
#ZCOMP            =  0
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP}
#
#Instrument.set_CAP(AMPLITUDE_P1,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 19 #####
####################  
#
## Configuration: 100 uF
#GENERATE_FUNCTION  = "CAP"
#AMPLITUDE_P1       =  0.0001
#ZCOMP              =  0
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP}
#
#Instrument.set_CAP(AMPLITUDE_P1,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 19 #####
####################  
#
## Configuration: 100 mF
#GENERATE_FUNCTION  = "CAP"
#AMPLITUDE_P1       =  0.1
#ZCOMP              =  2
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP}
#
#Instrument.set_CAP(AMPLITUDE_P1,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 20 #####
####################  
#
## Configuration: 100 °C WIRE2 RTD PT385_200
#GENERATE_FUNCTION  = "RTD"
#AMPLITUDE_P1       = 100
#ZCOMP              = 2
#RTD_TYPE           = "PT385_200"
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP,
#                    "RTD_TYPE"          :RTD_TYPE}
#
#Instrument.set_RTD(AMPLITUDE_P1,RTD_TYPE,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 21 #####
####################  
#
## Configuration: 100 °C WIRE4 RTD PT3916
#GENERATE_FUNCTION  = "RTD"
#AMPLITUDE_P1       = 100
#ZCOMP              = 4
#RTD_TYPE           = "PT3916"
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP,
#                    "RTD_TYPE"          :RTD_TYPE}
#
#Instrument.set_RTD(AMPLITUDE_P1,RTD_TYPE,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 22 #####
####################  
#
## Configuration: 100 °C NONE RTD CU10
#GENERATE_FUNCTION  = "RTD"
#AMPLITUDE_P1       = 100
#ZCOMP              = 0
#RTD_TYPE           = "CU10"
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "ZCOMP"             :ZCOMP,
#                    "RTD_TYPE"          :RTD_TYPE}
#
#Instrument.set_RTD(AMPLITUDE_P1,RTD_TYPE,ZCOMP)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 23 #####
####################  
#
## Configuration: 500 °C TC K
#GENERATE_FUNCTION  = "TC_OUT"
#AMPLITUDE_P1       = 500
#TC_TYPE            = "K"
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "TC_TYPE"           :TC_TYPE}
#
#Instrument.set_TC(AMPLITUDE_P1,TC_TYPE)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 24 #####
####################  
#
## Configuration: 100 °C TC R
#GENERATE_FUNCTION  = "TC_OUT"
#AMPLITUDE_P1       = 100
#TC_TYPE            = "R"
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "TC_TYPE"           :TC_TYPE}
#
#Instrument.set_TC(AMPLITUDE_P1,TC_TYPE)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
#
####################
###### TEST 26 #####
####################  
#
## Configuration: 1 V, 1 A @ 0 HZ
#GENERATE_FUNCTION  = "DC_POWER"
#AMPLITUDE_P1       = 1
#AMPLITUDE_P2       = 1
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "AMPLITUDE_P2"      :AMPLITUDE_P2} 
#
#Instrument.set_POWER_DC(AMPLITUDE_P1,AMPLITUDE_P2)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 27 #####
####################  
#
## Configuration: 100 V, 0.1 A @ 0 HZ
#GENERATE_FUNCTION   = "DC_POWER"
#AMPLITUDE_P1        = 100
#AMPLITUDE_P2        = 0.1
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION,
#                    "AMPLITUDE_P2"      :AMPLITUDE_P2} 
#
#Instrument.set_POWER_DC(AMPLITUDE_P1,AMPLITUDE_P2)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 28 #####
####################  
#
## Configuration: 1 V, 1 A @ 60 HZ
#GENERATE_FUNCTION  = "AC_POWER"
#AMPLITUDE_P1       = 1
#AMPLITUDE_P2       = 1
#FREQUENCY          = 60
#
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION, 
#                    "AMPLITUDE_P2"      :AMPLITUDE_P2,
#                    "FREQUENCY"         :FREQUENCY}
#
#Instrument.set_POWER_AC(AMPLITUDE_P1,AMPLITUDE_P2,FREQUENCY)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 29 #####
####################  
#
## Configuration: 100 V, 1 A @ 60 HZ
#GENERATE_FUNCTION    = "AC_POWER"
#AMPLITUDE_P1         = 100
#AMPLITUDE_P2         = 1
#FREQUENCY            = 60
#
#ConfigParameters = {"AMPLITUDE_P1"      :AMPLITUDE_P1,
#                    "GENERATE_FUNCTION" :GENERATE_FUNCTION, 
#                    "AMPLITUDE_P2"      :AMPLITUDE_P2,
#                    "FREQUENCY"         :FREQUENCY}
#
#Instrument.set_POWER_AC(AMPLITUDE_P1,AMPLITUDE_P2,FREQUENCY)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 30 #####
####################  
#
## Configuration: TC R
#GENERATE_FUNCTION  = "TC_MEAS"
#ConfigParameters = {"GENERATE_FUNCTION" :GENERATE_FUNCTION}
#
#Instrument.set_TCMEAS(TC_TYPE)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
####################
###### TEST 31 #####
####################  
#
## Configuration: TC T
#GENERATE_FUNCTION  = "TC_MEAS"
#ConfigParameters = {"GENERATE_FUNCTION" :GENERATE_FUNCTION}
#
#Instrument.set_TCMEAS(TC_TYPE)
## Checking for correct configuration
#TEST.test_configuration(ConfigParameters)
#
#
#

if __name__ == "__main__":
    unittest.main()