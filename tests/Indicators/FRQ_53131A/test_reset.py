import unittest
import sys
sys.path.append("../../../Indicators")
from FrequencyMeters import Counter_53131A 

## Test parameters
SIMULATION = False

## Una vez establecida la conexión, esperar 5 segundos, mandar
## comando de reset y después de 4 segundos pedir el ID.
## El comando es *RST

class ConfigurationTest(unittest.TestCase):
    ## Constats for test
    FUNCTION = {1:"DCV",2:"ACV",3:"ACDCV",4:"OHM",
                5:"OHMF",6:"DCI",7:"ACI",8:"ACDCI",
                9:"FREQ",10:"PER",11:"DSAC",12:"DSDC",
                13:"SSAC",14:"SSDC"}

    ## Available tests
#   FILTER
#   AUTO TRG   
#   SLOPE
#   SENSITIVITY 
#   GATE


## Start Multimeter and test enviroment
Instrument = Counter_53131A(bus_connection='GPIB0::3::INSTR',simulation=SIMULATION)
TEST = ConfigurationTest()
# Assign device to TEST
TEST.device = Instrument
