from fastembed import LateInteractionTextEmbedding
from qdrant_client import QdrantClient, models

model_name = "colbert-ir/colbertv2.0"
embedding_model = LateInteractionTextEmbedding(model_name)
qdrant_client = QdrantClient(url="http://10.81.53.217:6333/")

def create_collection():
    qdrant_client.create_collection(
        collection_name="constitution",
        vectors_config=models.VectorParams(
            size=128, #size of each vector produced by ColBERT
            distance=models.Distance.COSINE, #similarity metric between each vector
            multivector_config=models.MultiVectorConfig(
                comparator=models.MultiVectorComparator.MAX_SIM #similarity metric between multivectors (matrices)
            ),
        ),
    )

def get_embeddings(text:str):
    return embedding_model.embed(text)

def add_embeddings(id,article_id,vector ,text):
    qdrant_client.upload_points(
    collection_name="constitution",
    points=[
        models.PointStruct(
            id=id,
            payload={"id": article_id, "desc": text},
            vector=vector
        )
        for idx, vector in enumerate(vector)
    ],
)

def get_stage1(query:str):
    result = qdrant_client.query_points(
    collection_name="constitution",
    query=list(embedding_model.query_embed(query))[0],
    limit=50, 
    with_payload=True )
    return result
