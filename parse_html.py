import json
import glob
from bs4 import BeautifulSoup
from loguru import logger

# Logging configuration
logger.add("faq_extraction.log", rotation="1 MB", retention="1 week")

# Initialize a list to hold the extracted FAQs
all_faqs = []

# Find all HTML files in the specified directory
html_files = glob.glob("data/html/*.html")

logger.info(f"Found {len(html_files)} HTML files to process.")

for html_file in html_files:
    try:
        # Load the HTML content
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all sections that contain FAQ content
        faq_sections = soup.find_all("section")

        for section in faq_sections:
            # Extract the question from the <h3> or <h2> tag
            question_tag = section.find(["h2", "h3"])
            if question_tag:
                question = question_tag.get_text(strip=True)

                # Extract the answer, typically following the question
                answer = []
                for p in section.find_all(["p", "blockquote"]):
                    answer.append(p.get_text(strip=True))

                # Combine the answer paragraphs into a single string
                answer_text = " ".join(answer)

                # Add the extracted FAQ to the list
                all_faqs.append({
                    "question": question,
                    "answer": answer_text,
                    "source": html_file
                })

        logger.info(f"Processed file: {html_file}, extracted {len(faq_sections)} FAQ sections.")

    except Exception as e:
        logger.error(f"Failed to process file {html_file}: {e}")

# Save the extracted FAQs to a JSON file
output_file = "data/python_faqs.json"
try:
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(all_faqs, json_file, indent=4, ensure_ascii=False)
    logger.info(f"Successfully saved {len(all_faqs)} FAQs to {output_file}.")
except Exception as e:
    logger.error(f"Failed to save FAQs to {output_file}: {e}")
