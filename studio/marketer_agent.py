import json
from llm.llm import LLM
from extractor.json_object import extract_json_objects
from logger.logger import Logger
from pen.pen import pen


class MarketerAgent():
    def __init__(self, llm: LLM, log_level: str = "INFO"):
        self.llm = llm
        self.logger = Logger("marketer", pen.magenta_bright, log_level)
    
    def name(self) -> str:
        return self.llm.model_name

    def create_metadata(self, content) -> dict:
        self.logger.log("Creating metadata for content ...")
        resp = self.llm.send_message(
            f"""Generate a metadata for the following content draft, following the PROFESSIONAL CONTENT MANDATE, and OUTPUT CONSTRAINTS provided in your system instructions:

START OF CONTENT DRAFT--------------
{content}
END OF CONTENT DRAFT----------------""")
        json_data = extract_json_objects(resp)

        return json.loads(json_data[0])
