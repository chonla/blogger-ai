import os

from logger.logger import Logger
from pen.pen import pen
from .llm import LLM

class Gemini(LLM):
    def __init__(self, model_name: str, system_instruction: str = None):
        super().__init__(
            url=f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={os.getenv("GEMINI_API_KEY")}",
            headers={}
        )
        self.system_instruction = system_instruction
        self.history = []
        self.model_name = model_name
        self.logger = Logger("gemini", pen.magenta_bright)

    def send_message(self, prompt):
        conversation = {
            "role": "user",
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
        self.history.append(conversation)
        
        payload = {
            "system_instruction": {
                "parts": [
                    {
                    "text": self.system_instruction
                    }
                ]
            },
            "contents": self.history
        }

        resp = self.chat(payload)
        content = resp["candidates"][0]["content"]["parts"][0]["text"]
        
        self.logger.log_block("DEBUG Gemini Response Content", pen.gray(content))
        
        return content

    def clear_history(self):
        self.history = []