import DBFunctions as gtdb

class DriveTrain(object):

    def __init__(self, xcode):
        self.code = xcode
        self.dtID = 0
        self.desc = ''

    @property
    def code(self):
        return self.__code

    @code.setter
    def code (self, x):
        self.__code = x[:5]

class Manufacture(object):

    def __init__(self,name):
        self.name = name
        self.mfgID = 0

    def get(self,id):
        '''id = mfgID of the manufacture
        '''
        if id > 0:
            tmp_mfg = gtdb.get_manufacture(id)

        if len(tmp_mfg) > 0:
            r = tmp_mfg[0]
            self.mfgID = r[0]
            self.name = r[1]

class Category(object):

    def __init__(self,name):
        self.name = name
        self.catID = 0
        self.desc = ''

# class Car(object):
#     makeID= ''
#     make = ''
#     model = ''
#     year = ''
#     catID= ''
#     category = ''
#     dt_id =''
#     drivetrain = ''

#     def __init__(self,name):
#         self.name = name

#     pass

