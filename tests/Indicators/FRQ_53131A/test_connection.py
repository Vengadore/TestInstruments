from Indicators.FrequencyMeters import *
from time import sleep
import unittest

# Seleccionar un instrumento a travez de GPIB y mandar un comando
# simple de identificación, el instrumento debe responder con la
# información: HEWLETT-PACKARD, 53131A,0,XXXX
# El comando a mandar es *IDN?


class ConnectionTest(unittest.TestCase):
    def setup(self):
        self.Instrument = Counter_53131A(bus_connection='GPIB0::3::INSTR')

    def test_connection(self):
        self.setup()
        IDN = self.Instrument.get_IDN()
        self.assertEqual(IDN, "HEWLETT-PACKARD,53131A,0,4243")
        self.close_conection()

    def close_conection(self):
        self.Instrument.disconnect()


if __name__ == '__main__':
    unittest.main()
