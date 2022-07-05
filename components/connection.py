from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.flask_db
product_collection = db.Products

print('DB Connected')