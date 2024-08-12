from openai import OpenAI

class LLaMATextGenerator:
    def __init__(self, base_url, model='llama3'):
        self.client = OpenAI(base_url=base_url, api_key='ollama')
        self.model = model

    def generate_text(self, input_text: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{'role': 'user', 'content': input_text}],
            model=self.model,
        )
        return chat_completion.choices[0].message.content
