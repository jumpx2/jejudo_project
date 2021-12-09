import csv
import os
from pymongo import MongoClient


HOST = 'cluster0.c7lju.mongodb.net'
USER = 'jumpx2'
PASSWORD = '1234'
DATABASE_NAME = 'myFirstDatabase'
COLLECTION_NAME = 'jeju'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
coll_name = db[COLLECTION_NAME]

csv_file_name = 'jeju.csv'
current_path = os.path.join(os.getcwd(), csv_file_name)

int_col = ['base_year', 'user_count']

with open(current_path, 'r', encoding='UTF8') as file:
  reader = csv.DictReader(file)

  for row in reader:
    for keys in int_col:
      row[keys] = int(row[keys])
    coll_name.insert_one(row)

