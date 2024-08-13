import json
import glob
from bs4 import BeautifulSoup
from loguru import logger

logger.add("faq_extraction.log", rotation="1 MB", retention="1 week")

all_faqs = []

html_files = glob.glob("data/html/*.html")

logger.info(f"Found {len(html_files)} HTML files to process.")

for html_file in html_files:
    try:
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        faq_sections = soup.find_all("section")

        for section in faq_sections:
            question_tag = section.find(["h2", "h3"])
            if question_tag:
                question = question_tag.get_text(strip=True)

                answer = []
                for p in section.find_all(["p", "blockquote"]):
                    answer.append(p.get_text(strip=True))

                answer_text = " ".join(answer)

                all_faqs.append({
                    "question": question,
                    "answer": answer_text,
                    "source": html_file
                })

        logger.info(f"Processed file: {html_file}, extracted {len(faq_sections)} FAQ sections.")

    except Exception as e:
        logger.error(f"Failed to process file {html_file}: {e}")

output_file = "data/python_faqs.json"
try:
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(all_faqs, json_file, indent=4, ensure_ascii=False)
    logger.info(f"Successfully saved {len(all_faqs)} FAQs to {output_file}.")
except Exception as e:
    logger.error(f"Failed to save FAQs to {output_file}: {e}")
