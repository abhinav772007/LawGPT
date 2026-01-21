import pandas as pd
from embeddings import create_collection, get_embeddings, add_embeddings
from scripts.chunks import getChunks
df = pd.read_csv("hf://datasets/Sharathhebbar24/Indian-Constitution/Final_IC.csv")

create_collection()
counter = 0

for _, row in df.iterrows():
    document = row.to_dict()
    document["article_id"] = document["article_id"].split(' ')[1]
    article_chunks = getChunks(document["article_desc"])
    id = document["article_id"]
    print(f"getting embedding for {id}")

    for chunk in article_chunks:
        embed = list(get_embeddings(chunk))
        id = document["article_id"]
        print(id, counter)
        add_embeddings(counter,id,embed,chunk)
        counter +=1

print("Database and collection created successfully")

