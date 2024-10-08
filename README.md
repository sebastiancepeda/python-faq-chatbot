
# Python FAQ Conversational RAG Chatbot

This repository contains a Conversational Retrieval-Augmented Generation (RAG) chatbot designed to answer Python-related questions. The chatbot uses a FAISS index for efficient retrieval of relevant information and integrates with an LLM model for generating context-aware responses in a conversational manner.

## Demo

![Python FAQ Chatbot Demo](docs/streamlit-python-faq-chatbot.gif)

## Project Structure

```
python_faq_chatbot/
├── __init__.py
├── app.py
├── corpus.py
├── faiss_index.py
├── generators.py
├── rag.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── data/
    └── python_faqs.json
```

- `app.py`: Main entry point for the Streamlit web application.
- `corpus.py`: Contains the logic for loading the FAQ corpus.
- `faiss_index.py`: Manages the FAISS index and the `CorpusIndex` class.
- `generators.py`: Contains the logic for text generation using LLaMA or other models.
- `rag.py`: Implements the RAG system, including a conversational variant.
- `Dockerfile`: Dockerfile to containerize the Streamlit application.
- `docker-compose.yml`: Docker Compose file to manage the deployment of the application.
- `requirements.txt`: Lists the Python dependencies required for the project.
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

### Option 1: Running Locally (without Docker)

#### Create a Virtual Environment

It’s recommended to create a virtual environment to isolate dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

#### Configure the Environment

Install LLaMA >3.0 with Ollama: https://ollama.com/

### Option 2: Running with Docker (recommended)

#### Build and Run the Docker Container

1. **Ensure Docker and Docker Compose are installed** on your machine.
2. **Build and run the container** using Docker Compose:

   ```bash
   docker-compose up
   ```

This will build the Docker image (if not already built) and start the Streamlit application, making it accessible at `http://localhost:8501`.

### Interacting with the Chatbot

The chatbot interface allows you to input Python-related questions. The system will remember the conversation context, enabling a more natural interaction. The conversation history is displayed on the screen to provide context for ongoing interactions.

## Data

The `python_faqs.json` file contains frequently asked questions about Python. This data was sourced from the [Python Documentation](https://docs.python.org/3/) and is licensed under the Python Software Foundation License Version 2. Code examples and recipes in the data are additionally licensed under the Zero Clause BSD License.

## Contribution

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
