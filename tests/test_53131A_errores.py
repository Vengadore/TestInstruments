from Indicators.FrequencyMeters import *
from time import sleep
import unittest

# Lee por errores y espera que no existan errores:
# El comando es SYST:ERR?
# La respuesta es +0, “No error”

# Genera un error y espera leer el error


class ErrorTest(unittest.TestCase):
    def setup(self):
        self.Instrument = Counter_53131A(bus_connection='GPIB0::3::INSTR')

    def test_error(self):
        self.setup()
        ERROR = self.Instrument.get_ERROR()
        self.assertEqual(ERROR, '+0,"No error"')
        self.close_conection()

    def close_conection(self):
        self.Instrument.disconnect()


if __name__ == '__main__':
    unittest.main()
