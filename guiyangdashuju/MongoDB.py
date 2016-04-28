import pymongo

class DataBase(object):
    def __init__(self, db_name):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client[db_name]

    def get_db_handle(self):
        return self.db

    def get_sheet_handle(self, sheet_name):
        return self.db[sheet_name]