from fastembed.rerank.cross_encoder import TextCrossEncoder
from qdrant.embeddings import get_stage1
reranker = TextCrossEncoder(model_name='jinaai/jina-reranker-v1-turbo-en')

def get_reranked_results(query, top_k=10):
    initial = get_stage1(query)

    docs = []   # store description + file id together

    for i, hit in enumerate(initial.points):
        text = hit.payload["desc"]
        article_id = hit.payload["id"]

        print(f'Result number {i+1} is "{text}" (file={article_id})')

        docs.append({
            "article_id": article_id, "desc": text
        })

    # Extract descriptions for reranker
    descriptions = [d["desc"] for d in docs]

    # Rerank
    new_scores = list(reranker.rerank(query, descriptions))

    # Attach scores with index
    ranking = [(i, score) for i, score in enumerate(new_scores)]
    ranking.sort(key=lambda x: x[1], reverse=True)

    # Collect top file IDs
    top_files = []

    print("Reranked Results:")
    for rank_idx, (doc_idx, score) in enumerate(ranking[:top_k]):
        file_id = docs[doc_idx]["article_id"]
        desc = docs[doc_idx]["desc"]

        print(f'#{rank_idx+1} | score={score:.4f} | file={file_id}')
        print(f'    "{desc}"')

        top_files.append(file_id)

    return top_files
