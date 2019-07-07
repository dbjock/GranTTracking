import unittest
import logging
import logging.config
#Application required modules
from GranT import gtdb
from GranT import gtclasses as gt
from GranT import gtcfg

logging.config.fileConfig('logging.conf', defaults=None, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logging.info("==========================")

class TestMfgClass(unittest.TestCase):
    dbTest = "tests/test_GranTTSport.db"
    mydbConn = gtdb.create_connection(dbTest)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Istantiate(self):
        tstMfg = gt.Manufacture()
        self.assertEqual(tstMfg.id,0,"ID should be int 0")
        self.assertIsNone(tstMfg.name,"name should be none")

    def test_Load(self):
        tstMfg = gt.Manufacture()
        tstMfg.load(mydbConn,1)
        self.assert

if __name__ == '__main__':
    unittest.main()


