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

    def test_Getknown(self):
        theReturn = self.myDb.get_manufacture(1)
        self.assertGreater(len(theReturn),1,"One record with more than 1 element should have been returned")

    def test_GetNoRec(self):
        theReturn = self.myDb.get_manufacture(99999)
        self.assertIsNone(theReturn,"Expected no record to be returned")

    def test_GetnoInt(self):
        theReturn = self.myDb.get_manufacture("1")
        self.assertFalse(theReturn,"Expected false. Non integer was passed")

    def test_GetAllRecs(self):
        theReturn = self.myDb.get_manufacture(0)
        self.assertGreater(len(theReturn),3,"More than 3 elements should be return with all records")

    def test_CreateRec0(self):
        theReturn = self.myDb.write_manufacture(0,"Adding a New Record")
        self.assertTrue(theReturn,"Should have been able to create a new record")

    def test_CreateRec999(self):
        theReturn = self.myDb.write_manufacture(999,"Rec 999 added")
        self.assertTrue(theReturn,"Should have been able to create a new record 999")

    def test_CreateBlankName(self):
        theReturn = self.myDb.write_manufacture(0,"")
        self.assertFalse(theReturn,"Blank name should not be allowed")

    def test_CreateNoneName(self):
        theReturn = self.myDb.write_manufacture(0,None)
        self.assertFalse(theReturn,"Blank name should not be allowed")

    def test_CreateNonInt(self):
        theReturn = self.myDb.write_manufacture("A",'Testing Non number recID')
        self.assertFalse(theReturn,"Non INT recid should not be allowed")

    def test_UpdateRec(self):
        #TODO need to add query to ensure correct name comes back with recid
        theReturn = self.myDb.write_manufacture(2,"Updating Record")
        self.assertTrue(theReturn,"Record should have been updated")

if __name__ == '__main__':
    unittest.main()

logging.config.fileConfig('logging.conf', defaults=None, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logging.info("==========================")
logging.info(f"Testing Database: {gtcfg.dbcfg['dbFile']}")

