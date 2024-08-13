FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENV TOKENIZERS_PARALLELISM=false

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
