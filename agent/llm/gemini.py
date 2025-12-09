import json
import os

from pen.pen import pen
from .llm import LLM

class Gemini(LLM):
    def __init__(self, model_name: str, system_instruction: str = None):
        super().__init__(
            agent_name="gemini",
            agent_color=pen.blue_bright,
            url=f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers={},
            connection_timeout_seconds=int(os.getenv('CONNECTION_TIMEOUT_SECONDS', "15")),
            operation_timeout_seconds=int(os.getenv('OPERATION_TIMEOUT_SECONDS', "30"))
        )
        self.system_instruction = system_instruction
        self.history = []
        self.model_name = model_name

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
        
        self.logger.debug_block("Gemini Request Content", json.dumps(payload, ensure_ascii=False, indent=2))

        resp = self.chat(payload)
        content = resp["candidates"][0]["content"]["parts"][0]["text"]
        
        self.logger.debug_block("Gemini Response Content", content)
        
        return content

    def clear_history(self):
        self.history = []