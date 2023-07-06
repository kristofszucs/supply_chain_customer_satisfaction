from elasticsearch import Elasticsearch
import pandas as pd
import warnings
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

nltk.download('stopwords')
nltk.download('punkt')
print(stopwords.words('english'))

warnings.filterwarnings('ignore')

es = Elasticsearch(hosts = ["http://79.125.3.215:9200"])

query = {
    "query": {
        "match_all": {}
    },
    "size": 1000  # Adjust batch size as per your requirements
}

scroll = es.search(index="asurion", body=query, scroll="5m")
scroll_id = scroll["_scroll_id"]

hits = scroll["hits"]["hits"]
data = [hit["_source"] for hit in hits]

while len(hits) > 0:
    scroll = es.scroll(scroll_id=scroll_id, scroll="5m")
    hits = scroll["hits"]["hits"]
    data.extend([hit["_source"] for hit in hits])

df = pd.DataFrame(data)