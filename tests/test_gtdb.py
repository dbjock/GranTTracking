import unittest
import logging
import logging.config
#Application required modules
from GranT import gtdb

class TestMfg(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_CreateTable(self):
        myDBConnection = gtdb.create_connection(":memory:")
        self.assertTrue(gtdb.create_manufactures(myDBConnection),"Should have been able to create table")

    def test_writeNewRec(self):
        myDBConnection = gtdb.create_connection(":memory:")
        gtdb.create_manufactures(myDBConnection)
        self.assertTrue(gtdb.writeMfg(myDBConnection,0,"TheTest"),"Should have been able to write a record")

    def test_UpdateRec(self):
        myDBConnection = gtdb.create_connection(":memory:")
        gtdb.create_manufactures(myDBConnection)
        self.assertTrue(gtdb.writeMfg(myDBConnection,5,"TheTest"),"Should have been able to write a record")

    def test_getAllRec(self):
        myDBConnection = gtdb.create_connection(":memory:")
        gtdb.create_manufactures(myDBConnection)
        gtdb.writeMfg(myDBConnection,0,"TheTest")
        gtdb.writeMfg(myDBConnection,0,"TheTest1")
        gtdb.writeMfg(myDBConnection,0,"TheTest2")
        self.assertGreater(len(gtdb.getAllMfg(myDBConnection)),2,"Should get all the records")

    def test_getRec(self):
        myDBConnection = gtdb.create_connection(":memory:")
        gtdb.create_manufactures(myDBConnection)
        gtdb.writeMfg(myDBConnection,0,"TheTest")
        gtdb.writeMfg(myDBConnection,0,"TheTest1")
        gtdb.writeMfg(myDBConnection,0,"TheTest2")
        self.assertGreater(len(gtdb.getMfg(myDBConnection,1,key='recID')),1,"Should have got 1 record")

class TestTracks(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_CreateTable(self):
        myDBConnection = gtdb.create_connection(":memory:")
        self.assertTrue(gtdb.create_tracks(myDBConnection),"Should have been able to create table")

class TestDriveTrains(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_CreateTable(self):
        myDBConnection = gtdb.create_connection(":memory:")
        self.assertTrue(gtdb.create_driveTrains(myDBConnection),"Should have been able to create table")

class TestCircuits(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_CreateTable(self):
        myDBConnection = gtdb.create_connection(":memory:")
        self.assertTrue(gtdb.create_circuits(myDBConnection),"Should have been able to create table")

class TestCars(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_CreateTable(self):
        myDBConnection = gtdb.create_connection(":memory:")
        self.assertTrue(gtdb.create_cars(myDBConnection),"Should have been able to create table")

class TestCarCat(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_CreateTable(self):
        myDBConnection = gtdb.create_connection(":memory:")
        self.assertTrue(gtdb.create_carCats(myDBConnection),"Should have been able to create table")

if __name__ == '__main__':
    unittest.main()
