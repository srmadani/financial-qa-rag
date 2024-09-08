"""

This file prepares the dataframe and indexing for elastic search and saves the dataframe as a parquet file.

data reference: https://www.kaggle.com/datasets/yousefsaeedian/financial-q-and-a-10k

About Dataset
This dataset, titled "Financial-QA-10k", contains 10,000 question-answer pairs derived from company financial reports, specifically the 10-K filings. The questions are designed to cover a wide range of topics relevant to financial analysis, company operations, and strategic insights, making it a valuable resource for researchers, data scientists, and finance professionals. Each entry includes the question, the corresponding answer, the context from which the answer is derived, the company's stock ticker, and the specific filing year. The dataset aims to facilitate the development and evaluation of natural language processing models in the financial domain.

About the Dataset
Dataset Structure:

Rows: 7000
Columns: 5
question: The financial or operational question asked.
answer: The specific answer to the question.
context: The textual context extracted from the 10-K filing, providing additional information.
ticker: The stock ticker symbol of the company.
filing: The year of the 10-K filing from which the question and answer are derived.
Sample Data:

Question: What area did NVIDIA initially focus on before expanding into other markets?
Answer: NVIDIA initially focused on PC graphics.
Context: Since our original focus on PC graphics, we have expanded into various markets.
Ticker: NVDA
Filing: 2023_10K

Potential Uses:

Natural Language Processing (NLP): Develop and test NLP models for question answering, context understanding, and information retrieval.
Financial Analysis: Extract and analyze specific financial and operational insights from large volumes of textual data.
Educational Purposes: Serve as a training and testing resource for students and researchers in finance and data science.

License
Apache 2.0

preprocessing credit goes to: https://www.kaggle.com/code/banddaniel/financial-question-answering-w-gemma-2b-lora


"""

import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from tqdm import tqdm
SEED = 0
import os

file_path = 'db/df.parquet'
model = SentenceTransformer("all-mpnet-base-v2")

if os.path.exists(file_path):
    df = pd.read_parquet(file_path)
    print('====================================='*3)
    print('Data loaded from parquet file')
else:
    print('====================================='*3)
    print('Data not found. Preprocessing data...')
    data = pd.read_csv('db/Financial-QA-10k.csv')
    data.drop_duplicates(subset = ['question', 'answer'], inplace = True)
    data = data.sample(frac = 1, random_state = SEED).reset_index(drop = True)

    # preprocessing functions

    def text_preprocessing(text):
        text = str(text)
        text = text.lower()
        text = re.sub(r'\\W',' ',text) 
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        text = re.sub(r'http', ' ', text)
        text = re.sub(r'<.*?>+', ' ', text)
        text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', ' ', text)
        return text


    # applying preprocessing functions 
    full_data = data.copy()
    full_data['preprocessed_question'] = data['question'].apply(text_preprocessing)
    full_data['preprocessed_context'] = data['context'].apply(text_preprocessing)
    full_data['preprocessed_answer'] = data['answer'].apply(text_preprocessing)


    df = pd.DataFrame({
        'i' : full_data.index,
        'q' : full_data['preprocessed_question'],
        'q_': model.encode(full_data['preprocessed_question']).tolist(),
        'c' : full_data['preprocessed_context'],
        'c_': model.encode(full_data['preprocessed_context']).tolist(),
        'a' : full_data['preprocessed_answer'],
        'a_': model.encode(full_data['preprocessed_answer']).tolist(),
    })

    df.to_parquet('db/df.parquet')
    print('Data saved to parquet file')

# es_client = Elasticsearch('http://elasticsearch:9200', request_timeout=60)
es_client = Elasticsearch('http://elasticsearch:9200', request_timeout=60)


print('====================================='*3)
print('Elasticsearch client connected')

index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "q": {"type": "text"},
            "c": {"type": "text"},
            "q": {"type": "text"},
            "q_": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
            "c_": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
            "a_": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
        }
    }
}

index_name = "fin_qa"

es_client.indices.delete(index=index_name, ignore_unavailable=True)
es_client.indices.create(index=index_name, body=index_settings)

print('====================================='*3)
print('Index created')
for _, row in df.iterrows():
    es_client.index(index=index_name, document=row.to_dict())
print('====================================='*3)
print('Data indexed')