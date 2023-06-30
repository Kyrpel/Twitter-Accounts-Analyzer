from pymongo import MongoClient

class MongoDB:
    def __init__(self, db_ip, db_port, db_name):
        self.client = MongoClient(db_ip, db_port)
        self.db = self.client[db_name]

    def save_to_mongo(self, data, collection_name):
        collection = self.db[collection_name]
        return collection.insert_one(data)

    def find_one(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find_one(query)

    def update_one(self, collection_name, filter, update, upsert=False):
        collection = self.db[collection_name]
        return collection.update_one(filter, update, upsert=upsert)

    def get_collection(self, collection_name):
        return self.db[collection_name]
