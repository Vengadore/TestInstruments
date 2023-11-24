from Indicators.FrequencyMeters import *
from time import sleep
import unittest

# Una vez establecida la conexión, esperar 5 segundos, mandar
# comando de reset y después de 4 segundos pedir el ID.
# El comando es *RST


class ResetTest(unittest.TestCase):
    def setup(self):
        self.Instrument = Counter_53131A(bus_connection='GPIB0::3::INSTR')

    def test_reset(self):
        self.setup()
        self.Instrument.reset()
        self.close_conection()

    def close_conection(self):
        self.Instrument.disconnect()


if __name__ == '__main__':
    unittest.main()
