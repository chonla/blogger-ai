from llm.llm import LLM
from extractor.section import extract_section
from pen.pen import pen
from logger.logger import Logger


class WriterAgent():
    def __init__(self, llm: LLM, log_level: str = "INFO"):
        self.llm = llm
        self.logger = Logger("writer", pen.blue_bright, log_level)

    def name(self):
        return self.llm.model_name

    def write_content(self, topic: str, preferred_language: str):
        self.logger.log(f"Writing content for topic: {pen.yellow_bright(topic)} ...")
        content = self.llm.send_message(f"Write a blog entry about \"{topic}\" in {preferred_language} language following the PROFESSIONAL CONTENT MANDATE, SEO PROTOCOL, AD REVENUE OPTIMIZATION FOCUS, ARTICLE STRUCTURE, and OUTPUT CONSTRAINTS provided in your system instructions.")
        content = extract_section(content, "ARTICLE")
        return content
    
    def revise_content(self, overall_score: str, feedback: str):
        self.logger.log("Revising content based on editor feedback ...")
        revised_content = self.llm.send_message(
            f"""Revise the content draft recently submitted based on the following editor feedback, maintaining the original language, and using the score in the feedback to guide your revisions:\n
            
OVERALL SCORE TO LAST SUBMISSION:
{overall_score}

EDITOR FEEDBACK TO LAST SUBMISSION:
{feedback}"""
        )

        revised_content = extract_section(revised_content, "ARTICLE")
        return revised_content