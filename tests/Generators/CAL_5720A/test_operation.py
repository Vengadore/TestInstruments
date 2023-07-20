from Generators.cal5XXXA import *
import unittest
import time


class ConfigurationTest(unittest.TestCase):
    def setup(self):
        time.sleep(5)
        self.Instrument = FLUKE_5500A('GPIB0::0::INSTR')
        self.Instrument.reset()
        time.sleep(2)

    def close_conection(self):
        self.Instrument.disconnect()

    def test_operate(self):
        self.setup()
        self.Instrument.set_OHM(100000)
        self.Instrument.operate()
        estado = self.Instrument.status()
        self.assertEqual(estado, OPERATE_STATE,
                         "El calibrador no fue seteado")
        time.sleep(3)
        self.Instrument.stby()
        estado = self.Instrument.status()
        self.assertNotEqual(estado, OPERATE_STATE,
                            "El calibrador no fue seteado")
        time.sleep(3)
        self.close_conection()


if __name__ == '__main__':
    unittest.main()
