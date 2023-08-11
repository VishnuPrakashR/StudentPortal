#  Copyright (c) 2023. This is the property of Vishnu Prakash

"""
Database is handled here.
Multiple databases can be managed.
Starting with mongodb
"""
import pymongo


class Mongo:
    # Setting database
    def __init__(self, collection):
        server1 = self.server1 = pymongo.MongoClient("mongodb://172.17.0.5:27017/")
        database = server1['students-portal-db']
        self.collection = database[collection]

    # Get all values from defined collection
    def get(self, condition={}, limiter=None):
        collection = self.collection
        data = collection.find(condition, limiter)
        # self.server1.close()
        return data

    # Get all values from defined collection
    def find(self, condition={}, limiter=None):
        collection = self.collection
        data = collection.aggregate(condition)
        # self.server1.close()
        return data

    # Put data into collection
    def put(self, data):
        collection = self.collection
        response = collection.insert_one(data)
        # self.server1.close()
        return response

    # Put data into collection
    def putmany(self, data):
        collection = self.collection
        response = collection.insert_many(data)
        # self.server1.close()
        return response

    # Update data
    def set(self, condition, data, upsert=False):
        collection = self.collection
        response = collection.update_one(condition, {"$set": data}, upsert=upsert)
        # self.server1.close()
        return response

    # Update data
    def inc(self, condition, data, upsert=False):
        collection = self.collection
        response = collection.update(condition, {"$inc": data}, upsert=upsert)
        # self.server1.close()
        return response

    def setmany(self, condition, data, upsert=False):
        collection = self.collection
        response = collection.update_many(condition, {"$set": data}, upsert=upsert)
        # self.server1.close()
        return response

    # Returns only one value
    def getone(self, condition, limiter=None):
        collection = self.collection
        data = collection.find_one(condition, limiter)
        # self.server1.close()
        return data

    # Get data after updating the count
    def getaftercount(self, condition, counter):
        collection = self.collection
        updation = {"$inc": {counter: 1}}
        data = collection.find_one_and_update(condition, update=updation)
        # self.server1.close()
        return data

    def deleteMany(self, condition):
        response = self.collection.delete_many(condition)
        # self.server1.close()
        return response

    def removeElement(self, condition, data):
        response = self.collection.update_many(condition, {"$unset": data}, upsert=False)
        # self.server1.close()
        return response


# Testing functions
if __name__ == "__main__":
    pass

