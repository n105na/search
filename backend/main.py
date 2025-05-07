from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import nltk
from pydantic import BaseModel

from search_engine import (
    build_index,
    compute_tf,
    compute_df,
    compute_tfidf_matrix,
    preprocess,
    cosine_similarity,
    euclidean_distance
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://search-1-cq3x.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nltk.download('punkt')
nltk.download('stopwords')

indexed_docs = {
    "documents": [],
    "index": {},
    "tf": [],
    "idf": {},
    "tfidf": {}
}

@app.get("/")
def read_root():
    return {"message": "Backend is up and running!"}

@app.post("/index/")
async def index_documents(files: List[UploadFile] = File(...)):
    documents = []
    for file in files:
        if not file.filename.endswith(".txt"):
            return {"error": f"File {file.filename} is not a .txt file"}
        content = await file.read()
        decoded = content.decode("utf-8")
        documents.append(decoded)
    
    if not documents:
        return {"error": "No valid .txt files uploaded"}

    index = build_index(documents)
    tf_scores = compute_tf(documents)
    idf_scores = compute_df(index, len(documents))
    tfidf_matrix = compute_tfidf_matrix(tf_scores, idf_scores, len(documents))

    indexed_docs["documents"] = documents
    indexed_docs["index"] = index
    indexed_docs["tf"] = tf_scores
    indexed_docs["idf"] = idf_scores
    indexed_docs["tfidf"] = tfidf_matrix

    return {"message": "Indexing completed successfully"}

@app.get("/view-index/")
def view_index():
    if not indexed_docs["index"]:
        return {"error": "No index built yet"}
    return indexed_docs

class SearchQuery(BaseModel):
    query: str
    metric: str  # "cosine" or "euclidean"

@app.post("/search/")
def search_documents(search: SearchQuery):
    if not indexed_docs["tfidf"]:
        return {"error": "No documents indexed yet"}

    query_tokens = preprocess(search.query)
    query_freq = {}
    for token in query_tokens:
        query_freq[token] = query_freq.get(token, 0) + 1

    max_freq = max(query_freq.values(), default=1)
    query_tf = {term: count / max_freq for term, count in query_freq.items()}

    query_vector = []
    terms = list(indexed_docs["tfidf"].keys())
    for term in terms:
        tf = query_tf.get(term, 0.0)
        idf = indexed_docs["idf"].get(term, 0.0)
        query_vector.append(tf * idf)

    results = []
    for doc_id in range(len(indexed_docs["documents"])):
        doc_vector = [indexed_docs["tfidf"][term][doc_id] for term in terms]

        if search.metric == "cosine":
            score = cosine_similarity(query_vector, doc_vector)
        elif search.metric == "euclidean":
            score = euclidean_distance(query_vector, doc_vector)
        else:
            return {"error": "Invalid metric"}

        results.append((doc_id, score))

    reverse = True if search.metric == "cosine" else False
    results.sort(key=lambda x: x[1], reverse=reverse)

    return {
        "results": [
            {
                "doc_id": doc_id,
                "score": score,
                "content": indexed_docs["documents"][doc_id]
            } for doc_id, score in results
        ]
    }