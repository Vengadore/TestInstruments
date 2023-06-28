from time import sleep
import unittest
import sys
sys.path.append("./Generators")
from cal5XXXA import FLUKE_5500A, OPERATE_STATE

    ## Available tests
#   FILTER
#   LEVEL
#   AUTO TRG   
#   SLOPE
#   SENSITIVITY 
#   GATE 

class ConfigurationTest(unittest.TestCase):
    def setup(self):
        sleep(5)
        self.Instrument = FLUKE_5500A(0)
        self.Instrument.reset()
        sleep(2)
    
    def close_conection(self):
        self.Instrument.disconnect()

    def test_operate(self):
        self.setup()
        self.Instrument.set_OHM(100000)
        self.Instrument.operate()
        estado = self.Instrument.status()
        self.assertEqual(estado, OPERATE_STATE,
                         "El calibrador no fue seteado")
        sleep(3)
        self.Instrument.stby()
        estado = self.Instrument.status()
        self.assertNotEqual(estado, OPERATE_STATE,
                         "El calibrador no fue seteado")
        sleep(3)
        self.close_conection()


       

if __name__ == '__main__':
    unittest.main()
    