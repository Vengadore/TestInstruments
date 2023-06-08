import unittest
import sys
sys.path.append("../../../Indicators")
from FrequencyMeters import Counter_53131A 

## Una vez establecida la conexión, esperar 5 segundos, mandar
## comando de reset y después de 4 segundos pedir el ID.
## El comando es *RST

class ConfigurationTest(unittest.TestCase):
    def setup(self):
        self.Instrument = Counter_53131A(bus_connection='GPIB0::3::INSTR')

    def test_reset(self):
        self.setup()
        self.Instrument.reset()
