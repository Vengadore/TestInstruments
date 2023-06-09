import unittest
import sys
sys.path.append("./Indicators")
from FrequencyMeters import Counter_53131A 

    ## Available tests
#   FILTER
#   AUTO TRG   
#   SLOPE
#   SENSITIVITY 
#   GATE 

class ConfigurationTest(unittest.TestCase):
    def setup(self):
        self.Instrument = Counter_53131A(bus_connection='GPIB0::3::INSTR')

    

if __name__ == '__main__':
    unittest.main()