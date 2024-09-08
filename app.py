import streamlit as st
import time
from elasticsearch import Elasticsearch
from ollama import Client

client = Client(host='http://ollama:11434')
es_client = Elasticsearch('http://elasticsearch:9200')

def elastic_search(query, index_name='fin_qa'):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["q^3", "a", "c^0.5"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs

def build_prompt(query, search_results):
    prompt_template = """
You're a financial assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    
    for doc in search_results:
        context += f"question: {doc['q']}\nanswer: {doc['a']}\ncontext: {doc['c']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

def llm(prompt):
    response = client.chat(model='qwen2:0.5b', messages=[{
                'role': 'user',
                'content': prompt,
                },])
    
    return response['message']['content']

def rag(query):
    search_results = elastic_search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer

def main():
    st.title("Financial Q&A System")
    st.write("""
    This application leverages a dataset containing 10,000 financial question-answer pairs derived from 10-K filings. It is designed to answer your financial queries using a combination of ElasticSearch and a local LLM model. The dataset covers a wide range of topics relevant to financial analysis and company operations.
    
    **Potential Uses:**
    - Develop and test NLP models for question answering and context understanding.
    - Extract and analyze specific financial insights.
    - Serve as a resource for educational purposes in finance and data science.
    """)
    
    user_input = st.text_input("Enter your query:")

    if st.button("Ask"):
        with st.spinner('Processing...'):
            output = rag(user_input)
            st.success("Completed!")
            st.write(output)

if __name__ == "__main__":
    main()