import os
from .llm import LLM
from pen.pen import pen
from logger.logger import Logger

class OpenAI(LLM):
    def __init__(self, model_name: str, system_instruction: str = None):
        super().__init__(
            url=f"https://api.openai.com/v1/chat/completions",
            headers={ "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}" }
        )
        self.system_instruction = system_instruction
        self.history = []
        self.model_name = model_name
        self.logger = Logger("openai", pen.yellow_bright)

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
        
        self.logger.log_block("DEBUG OpenAI Response Content", pen.gray(content))
        
        return content

    def clear_history(self):
        self.history = []