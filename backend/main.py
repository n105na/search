from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store state
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

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    contents = []
    for file in files:
        if file.filename.endswith(".txt"):
            file_content = await file.read()
            decoded = file_content.decode("utf-8")
            contents.append({"filename": file.filename, "content": decoded})
        else:
            contents.append({"filename": file.filename, "error": "Only .txt files allowed"})
    return contents

class DocumentSet(BaseModel):
    documents: list[str]

@app.post("/index/")
def index_documents(doc_set: DocumentSet):
    documents = doc_set.documents
    index = build_index(documents)
    tf_scores = compute_tf(documents)
    idf_scores = compute_df(index, len(documents))
    tfidf_matrix = compute_tfidf_matrix(tf_scores, idf_scores, len(documents))

    indexed_docs["documents"] = documents
    indexed_docs["index"] = index
    indexed_docs["tf"] = tf_scores
    indexed_docs["idf"] = idf_scores
    indexed_docs["tfidf"] = tfidf_matrix

    return {
        "index": {k: list(v) for k, v in index.items()},
        "tfidf": {k: v for k, v in tfidf_matrix.items()}
    }

@app.get("/view-index/")
def view_index():
    if not indexed_docs["index"]:
        raise HTTPException(status_code=404, detail="No index built yet")
    return indexed_docs

class SearchQuery(BaseModel):
    query: str
    metric: str  # "cosine" or "euclidean"

@app.post("/search/")
def search_documents(search: SearchQuery):
    if not indexed_docs["tfidf"]:
        raise HTTPException(status_code=400, detail="No documents indexed yet")

    query_tokens = preprocess(search.query)
    query_freq = {}
    for token in query_tokens:
        query_freq[token] = query_freq.get(token, 0) + 1

    max_freq = max(query_freq.values(), default=1)
    query_tf = {term: count / max_freq for term, count in query_freq.items()}

    # Compute query TF-IDF vector
    query_vector = []
    terms = list(indexed_docs["tfidf"].keys())
    for term in terms:
        tf = query_tf.get(term, 0.0)
        idf = indexed_docs["idf"].get(term, 0.0)
        query_vector.append(tf * idf)

    # Build document vectors
    results = []
    for doc_id in range(len(indexed_docs["documents"])):
        doc_vector = [indexed_docs["tfidf"][term][doc_id] for term in terms]

        if search.metric == "cosine":
            score = cosine_similarity(query_vector, doc_vector)
        elif search.metric == "euclidean":
            score = euclidean_distance(query_vector, doc_vector)
        else:
            raise HTTPException(status_code=400, detail="Invalid metric")

        results.append((doc_id, score))

    # Sort results (reverse for cosine, normal for euclidean)
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