
# Python FAQ Conversational RAG Chatbot

This repository contains a Conversational Retrieval-Augmented Generation (RAG) chatbot designed to answer Python-related questions. The chatbot uses a FAISS index for efficient retrieval of relevant information and integrates with an LLM model for generating context-aware responses in a conversational manner.

## Project Structure

```
python_faq_chatbot/
├── __init__.py
├── app.py
├── corpus.py
├── faiss_index.py
├── generators.py
├── rag.py
└── data/
    └── python_faqs.json
```

- `app.py`: Main entry point for the Streamlit web application.
- `corpus.py`: Contains the logic for loading the FAQ corpus.
- `faiss_index.py`: Manages the FAISS index and the `CorpusIndex` class.
- `generators.py`: Contains the logic for text generation using LLaMA or other models.
- `rag.py`: Implements the RAG system, including a conversational variant.
- `data/python_faqs.json`: JSON file containing the Python FAQs used by the system.

## Features

- **Conversational RAG**: The system maintains conversation context, enabling follow-up questions and contextually relevant responses.
- **Efficient Retrieval**: Uses FAISS for fast and scalable similarity search, ensuring relevant documents are retrieved quickly.
- **LLM Integration**: Integrates with a Large Language Model (LLM) to generate human-like responses based on the retrieved documents and conversation history.

## Installation

### Clone the Repository

```bash
git clone git@github.com:sebastiancepeda/python-faq-chatbot.git
cd python-faq-chatbot
```

### Create a Virtual Environment

It’s recommended to create a virtual environment to isolate dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Configure the Environment

Install Llama >3.0 with Ollama: https://ollama.com/

## Usage

### Running the Chatbot

You can start the chatbot by running:

```bash
streamlit run app.py
```

This will launch the chatbot in your web browser, accessible at `http://localhost:8501`.

### Interacting with the Chatbot

The chatbot interface allows you to input Python-related questions. The system will remember the conversation context, enabling a more natural interaction. The conversation history is displayed on the screen to provide context for ongoing interactions.

## Contribution

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
