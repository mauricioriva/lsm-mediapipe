import pymongo


class Database:
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['<DB NAME>']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)
