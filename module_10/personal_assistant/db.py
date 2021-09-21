import pymongo
from pymongo.database import Database
from pymongo.collection import Collection


# Mongo
_CONNECTION = "mongodb://admin:qwe123@localhost:27017/personal_assistant_db?retryWrites=true&w=majority"
# client
mongo_client = pymongo.MongoClient(_CONNECTION)
# db
personal_assistant_db: Database = mongo_client.personal_assistant_db
# collection
contacts_collection: Collection = personal_assistant_db.contacts
