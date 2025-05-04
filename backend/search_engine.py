import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict
import math
import json

nltk.download("stopwords")
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text

def tokenize(text):
    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [stemmer.stem(word) for word in words]
    return words

def preprocess(text):
    return tokenize(clean_text(text))

def compute_tf(documents):
    tf_list = []
    for text in documents:
        tokens = preprocess(text)
        if not tokens:
            tf_list.append({})
            continue
        freq_dict = defaultdict(int)
        for token in tokens:
            freq_dict[token] += 1
        max_freq = max(freq_dict.values())
        tf_normalized = {term: count / max_freq for term, count in freq_dict.items()}
        tf_list.append(tf_normalized)
    return tf_list

def compute_df(index, total_docs):
    idf = {}
    for term, docs in index.items():
        df = len(docs)
        idf[term] = math.log2(total_docs / df) if df > 0 else 0
    return idf

def compute_global_tf(tf_list, all_terms, total_docs):
    tf_global = defaultdict(lambda: [0.0] * total_docs)
    for doc_id, tf_doc in enumerate(tf_list):
        for term in all_terms:
            if term in tf_doc:
                tf_global[term][doc_id] = tf_doc[term]
    return dict(tf_global)

def compute_tfidf_matrix(tf_list, idf, total_docs):
    tfidf_matrix = defaultdict(lambda: [0.0] * total_docs)
    for doc_id, tf_doc in enumerate(tf_list):
        for term, freq in tf_doc.items():
            if term in idf:
                tfidf_matrix[term][doc_id] = freq * idf[term]
    return dict(tfidf_matrix)

def build_index(documents):
    index = defaultdict(set)
    for doc_id, text in enumerate(documents):
        tokens = preprocess(text)
        for token in tokens:
            index[token].add(doc_id)
    return {term: sorted(list(doc_ids)) for term, doc_ids in index.items()}

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def euclidean_distance(vec1, vec2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))

