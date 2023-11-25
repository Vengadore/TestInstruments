import sys
import os

# Add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Generators.cal5XXXA import *
import unittest
import time

    ## Available tests
#   FILTER
#   LEVEL
#   AUTO TRG   
#   SLOPE
#   SENSITIVITY 
#   GATE 

SIMULATION = True

class ConfigurationTest(unittest.TestCase):
    def setup(self):
        time.sleep(5) if not SIMULATION else None
        bus = "MOCK0::mock1::INSTR" if SIMULATION else "GPBI0::4::INSTR"
        self.Instrument = FLUKE_5500A(bus, simulation=SIMULATION)
        self.Instrument.reset()
        time.sleep(2) if not SIMULATION else None
    
    def close_conection(self):
        self.Instrument.disconnect()

    def test_operate(self):
        self.setup()
        self.Instrument.set_OHM(100000)
        self.Instrument.operate()
        estado = self.Instrument.status()
        self.assertEqual(estado, OPERATE_STATE,
                         "El calibrador no fue seteado")
        time.sleep(3) if not SIMULATION else None
        self.Instrument.stby()
        estado = self.Instrument.status()
        self.assertNotEqual(estado, OPERATE_STATE,
                         "El calibrador no fue seteado")
        time.sleep(3) if not SIMULATION else None
        self.close_conection()


       

if __name__ == '__main__':
    unittest.main()
    