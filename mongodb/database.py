import pandas as pd
from pymongo import MongoClient

df = pd.read_csv("hf://datasets/Sharathhebbar24/Indian-Constitution/Final_IC.csv")
client = MongoClient("mongodb://admin:admin123@10.81.53.217:27017/?authSource=admin")

db = client["lawgpt_db"]
collection = db["articles"]

for _, row in df.iterrows():
    document = row.to_dict()
    document["article_id"] = document["article_id"].split(' ')[1]
    collection.insert_one(document)

print("Database and collection created successfully")