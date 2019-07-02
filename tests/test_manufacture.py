import unittest
import logging
import logging.config
#Application required modules
from GranT import DBClass
from GranT import GTClasses as gt
from GranT import config as gtcfg

class TestMfgClass(unittest.TestCase):

    myDb = DBClass.GtDB(gtcfg.dbcfg['dbFile'])
    tstObj = gt.Manufacture(myDb)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_LoadInt(self):
        self.tstObj.load(1)
        self.assertEqual(self.tstObj.name,'Jaguar')
        return

class TestMfgDatabase(unittest.TestCase):
    myDb = DBClass.GtDB(gtcfg.dbcfg['dbFile'])

    def test_known(self):
        theReturn = self.myDb.get_manufacture(1)
        self.assertGreater(len(theReturn),1,"One record with more than 1 element should have been returned")

    def test_NoRec(self):
        theReturn = self.myDb.get_manufacture(99999)
        self.assertIsNone(theReturn,"Expected no record to be returned")

    def test_noInt(self):
        theReturn = self.myDb.get_manufacture("1")
        self.assertFalse(theReturn,"Expected false. Non integer was passed")

    def test_AllRecs(self):
        theReturn = self.myDb.get_manufacture(0)
        self.assertGreater(len(theReturn),3,"More than 3 elements should be return with all records")

if __name__ == '__main__':
    unittest.main()

logging.config.fileConfig('logging.conf', defaults=None, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logging.info("TEsting stuff loaded")

