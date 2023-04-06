from pymongo import MongoClient

# client = MongoClient("mongodb://<username>:<password>@<host>:<port>/<database>")
# db = client["my_database"]
client = MongoClient('mongodb+srv://subbareddy:subbareddy123@cluster0.yjrvgmv.mongodb.net/test')
db = client['scmxpertlite']
signup_collection=db['users']
shipment_collection = db['shipment']