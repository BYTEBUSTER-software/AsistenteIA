from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def search_events(events, query: str):
    corpus = [e.description for e in events]
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)[0]
    
    return [events[i["corpus_id"]] for i in hits]
