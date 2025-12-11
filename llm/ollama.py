import os
import re
from .llm import LLM
from pen.pen import pen


class Ollama(LLM):
    def __init__(self, model_name: str, system_instruction: str = None):
        super().__init__(
            agent_name="ollama",
            agent_color=pen.magenta_bright,
            url=f"{os.getenv('OLLAMA_API_BASE_URL')}/api/chat",
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
            "content": prompt
        }
        self.history.append(conversation)
        
        payload = {
            "model": self.model_name,
            "stream": False,
            "tools": [],
            "messages": [
                {
                    "role": "system",
                    "content": self.system_instruction
                }
            ] + self.history
        }

        resp = self.chat(payload)
        content = resp["message"]["content"]

        content = content.strip()
        
        # Some models may return JSON wrapped in markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
            if "```" in content:
                content = content.rsplit("```", 1)[0]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        # Some models does not properly handle new lines in JSON
        if "\n" in content:
            # Remove leading/trailing new lines
            content = re.sub(r"^\n", '\n', content)

        self.logger.debug_block("DEBUG Ollama Response Content", content)

        return content

    def clear_history(self):
        self.history = []