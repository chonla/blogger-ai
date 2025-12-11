from abc import abstractmethod
import json
import os
from typing import Dict
import time
import pycurl
from io import BytesIO

from logger.logger import Logger


class LLM:
    def __init__(self, agent_name: str, agent_color: str, url: str, headers: Dict[str, str], connection_timeout_seconds: int = 15, operation_timeout_seconds: int = 20):
        self.url = url
        self.headers = { "Content-Type": "application/json" } | headers
        self.model_name = "unnamed-model"
        self.connection_timeout_seconds = connection_timeout_seconds
        self.operation_timeout_seconds = operation_timeout_seconds
        self.logger = Logger(agent_name, agent_color)
        self.curl_verbose = 0 if os.getenv("CURL_VERBOSE", "false").upper() == "FALSE" else 1

    def chat(self, payload):
        start_of_content_writing_time = time.time()
        curl_client = pycurl.Curl()
        curl_client.setopt(pycurl.CONNECTTIMEOUT, self.connection_timeout_seconds)
        curl_client.setopt(pycurl.TIMEOUT, self.operation_timeout_seconds)
        curl_client.setopt_string(pycurl.URL, self.url)
        curl_client.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V4)
        curl_client.setopt(pycurl.POST, 1)
        curl_client.setopt_string(pycurl.POSTFIELDS, json.dumps(payload))
        header_list = [f"{key}: {value}" for key, value in self.headers.items()]
        curl_client.setopt(pycurl.HTTPHEADER, header_list)
        response_buffer = BytesIO()
        curl_client.setopt(pycurl.WRITEFUNCTION, response_buffer.write)
        curl_client.setopt(pycurl.FOLLOWLOCATION, True)
        curl_client.setopt(pycurl.ACCEPT_ENCODING, "gzip, deflate")
        curl_client.setopt(pycurl.VERBOSE, self.curl_verbose)
        curl_client.setopt_string(pycurl.PROXY, "")
        curl_client.perform()
        curl_client.close()
        response_data = response_buffer.getvalue().decode('utf-8')
        end_of_content_writing_time = time.time()
        self.logger.log_time_taken(end_of_content_writing_time - start_of_content_writing_time)
        return json.loads(response_data)
    
    @abstractmethod
    def send_message(self, prompt, preferred_language="English"):
        pass

    @abstractmethod
    def clear_history(self):
        pass

