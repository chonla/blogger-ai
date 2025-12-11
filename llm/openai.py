import os
from .llm import LLM
from pen.pen import pen


class OpenAI(LLM):
    def __init__(self, model_name: str):
        super().__init__(
            provider_name="openai",
            provider_color=pen.yellow_bright,
            url=f"https://api.openai.com/v1/chat/completions",
            headers={ "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}" },
            connection_timeout_seconds=int(os.getenv('CONNECTION_TIMEOUT_SECONDS', "15")),
            operation_timeout_seconds=int(os.getenv('OPERATION_TIMEOUT_SECONDS', "30"))
        )
        self.history = []
        self.model_name = model_name

    def send_message(self, prompt):
        conversation = {
            "role": "user",
            "content": prompt
        }
        self.history.append(conversation)
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": self.system_instruction
                }
            ] + self.history
        }

        resp = self.chat(payload)
        content = resp["choices"][0]["message"]["content"]
        
        self.logger.debug_block("DEBUG OpenAI Response Content", content)
        
        return content

    def clear_history(self):
        self.history = []