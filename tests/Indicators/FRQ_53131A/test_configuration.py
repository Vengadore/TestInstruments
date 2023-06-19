import unittest
import sys
sys.path.append("./Indicators")
from FrequencyMeters import Counter_53131A 

    ## Available tests
#   FILTER
#   LEVEL
#   AUTO TRG   
#   SLOPE
#   SENSITIVITY 
#   GATE 

class ConfigurationTest(unittest.TestCase):
    def setup(self):
        self.Instrument = Counter_53131A(bus_connection='GPIB0::3::INSTR')

    def close_conection(self):
        self.Instrument.disconnect()

    def test_configure_Filter(self):
        self.setup()
        self.Instrument.set_LPF()
        estado = self.Instrument.inst.query(":INP1:FILT:LPAS:STAT?")
        self.assertCountEqual(estado,"1")
        self.close_conection()

    def test_configure_Level(self):
        self.setup()
        self.Instrument.set_Level(2)
        tension = self.Instrument.inst.query(":SENS:EVEN1:LEV:ABS?")
        self.assertEqual(float(tension),2.0)
        self.close_conection()
    
    def test_configure_SLOPE(self):
        self.setup()
        self.Instrument.set_SLOPE("POS")
        pol = self.Instrument.inst.query(":SENS:EVEN1:SLOP?")
        self.assertEqual(pol,"POS")
        self.close_conection()

    def test_configure_SENSTVTY(self):
        self.setup()
        self.Instrument.set_SENSTVTY("LO")
        sens = self.Instrument.inst.query(":SENS:EVEN1:HYST:REL?")
        self.assertEqual(sens,'+100')
        self.close_conection()

    def test_configure_COUPLING(self):
        self.setup()
        self.Instrument.set_COUPLING("DC")
        coup = self.Instrument.inst.query(":INP:COUP?")
        self.assertEqual(coup,"DC")
        self.close_conection()
    
    def test_configure_IMPEDANCE(self):
        self.setup()
        self.Instrument.set_IMPEDANCE('50 OHM')
        imp = self.Instrument.inst.query(":INP1:IMP?")
        self.assertEqual(float(imp),50.0)
        self.close_conection()

    def test_configure_Gate_Time(self):
        self.setup()
        self.Instrument.set_Gate_Time(1.000)
        tension = self.Instrument.inst.query(":FREQ:ARM:STOP:TIM?")
        self.assertEqual(float(tension),1.0)
        self.close_conection()

    

if __name__ == '__main__':
    unittest.main()