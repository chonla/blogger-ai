from abc import abstractmethod
import json
from typing import Dict

import requests


class LLM:
    def __init__(self, url: str, headers: Dict[str, str]):
        self.url = url
        self.headers = { "Content-Type": "application/json" } | headers

    def chat(self, payload):
        payload_body = json.dumps(payload)
        
        resp = requests.post(self.url, headers=self.headers, data=payload_body)
        resp.raise_for_status()

        data = resp.json()
        return data
    
    @abstractmethod
    def send_message(self, prompt, preferred_language="English"):
        pass

    @abstractmethod
    def clear_history(self):
        pass

