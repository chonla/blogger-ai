import json
from llm.llm import LLM
from extractor.section import extract_section
from pen.pen import pen
from logger.logger import Logger
from extractor.json_object import extract_json_objects


class EditorAgent():
    def __init__(self, llm: LLM, log_level: str = "INFO"):
        self.llm = llm
        self.logger = Logger("editor", pen.green_bright, log_level)

    def name(self):
        return self.llm.model_name

    def review_content(self, content):
        self.logger.log("Reviewing content draft ...")
        entry_submission = f"""The content draft below has been submitted in JSON format. Please review the following content, focusing on title and body, and provide your detailed feedback and suggested edits to enhance its quality:
START OF CONTENT DRAFT--------------
{content}
END OF CONTENT DRAFT----------------"""
        
        feedback = self.llm.send_message(entry_submission)
        
        score_json_str = extract_section(feedback, "FEEDBACK JSON")
        if score_json_str == "":
            score_json = extract_json_objects(feedback)
        else:
            score_json = extract_json_objects(score_json_str)
        overall_score = extract_section(feedback, "OVERALL SCORE")
        suggested_feedback = extract_section(feedback, "SUGGESTED FEEDBACK")
        
        result = {
            "score": json.loads(score_json[0]),
            "overall_score": overall_score,
            "suggested_feedback": suggested_feedback
        }
        return result
