# Financial Q&A RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for answering financial questions based on data from 10-K filings. It combines ElasticSearch for efficient information retrieval with a local Language Model (LLM) to generate accurate and context-aware responses to financial queries.

## Features

- Uses a dataset of 10,000 financial question-answer pairs derived from 10-K filings
- Implements a RAG architecture using ElasticSearch and Ollama
- Provides a user-friendly interface using Streamlit
- Fully dockerized for easy deployment and scalability

## How It Works

1. **Data Preparation**: The system preprocesses the financial Q&A dataset and indexes it in ElasticSearch.
2. **Query Processing**: When a user submits a question, the system retrieves relevant context from ElasticSearch.
3. **Answer Generation**: The retrieved context is then passed to a local LLM (Qwen 0.5b) to generate a response.
4. **User Interface**: The generated answer is displayed to the user through a Streamlit web interface.

## Prerequisites

- Docker
- Docker Compose

## Setup and Running

1. Clone the repository:
   ```bash
   git clone https://github.com/srmadani/financial-qa-rag.git
   cd financial-qa-rag
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Once all services are up, access the application at `http://localhost:8501`

## Usage

1. Open your web browser and navigate to `http://localhost:8501`
2. Enter your financial question in the text input field
3. Click "Ask" to submit your query
4. The system will process your question and display the answer

## Project Structure

- `app.py`: Main Streamlit application
- `data_prep.py`: Data preprocessing and ElasticSearch indexing
- `Dockerfile`: Instructions for building the Docker image
- `docker-compose.yaml`: Defines and configures the Docker services
- `requirements.txt`: Lists the Python dependencies
- `wait-for-elasticsearch.sh`: Ensures ElasticSearch is ready before starting the app

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Acknowledgements

- Dataset source: [Kaggle - Financial Q&A 10k](https://www.kaggle.com/datasets/yousefsaeedian/financial-q-and-a-10k)
- Preprocessing credit: [Kaggle Notebook](https://www.kaggle.com/code/banddaniel/financial-question-answering-w-gemma-2b-lora)
- RAG design credit: [DataTalksClub/llm-zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)

## Disclaimer

This system is designed for educational and research purposes. Always consult with qualified financial professionals for actual financial advice.
