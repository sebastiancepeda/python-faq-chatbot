import json
from loguru import logger

def load_corpus(file_path):
    logger.info(f"Loading the FAQs corpus from {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        faqs_data = json.load(file)
    logger.info(f"Successfully loaded {len(faqs_data)} FAQs.")

    corpus = [
        f"Question: {faq['question']} Answer: {faq['answer']} Source: {faq['source']}"
        for faq in faqs_data
    ]
    return corpus
