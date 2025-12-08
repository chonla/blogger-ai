import json
import os
from agent.editor_agent import EditorAgent
from agent.seo_agent import SEOAgent
from agent.writer_agent import WriterAgent
from publisher.markdown import MarkdownPublisher
from logger.logger import Logger
from pen.pen import pen


class BlogStudio:
    def __init__(self, writer: WriterAgent, editor: EditorAgent, seo: SEOAgent, publisher: MarkdownPublisher):
        self.writer = writer
        self.editor = editor
        self.seo = seo
        self.publisher = publisher
        self.logger = Logger("studio", pen.cyan_bright)
        
    def create_blog_post(self, topic: str):
        review_limit = int(os.getenv("BLOG_REVIEW_LIMIT", "5"))
        quality_threshold = float(os.getenv("MINIMUM_QUALITY_SCORE", "4.5"))
        self.logger.log(f"writer: {pen.yellow_bright(self.writer.name())}")
        self.logger.log(f"editor: {pen.yellow_bright(self.editor.name())}")
        self.logger.log(f"seo: {pen.yellow_bright(self.seo.name())}")
        self.logger.log(f"publisher: {pen.yellow_bright('MarkdownPublisher')}")
        self.logger.log(f"minimum quality score: {pen.yellow_bright(str(quality_threshold))}")
        self.logger.log(f"review limit: {pen.yellow_bright(str(review_limit))}")

        self.logger.log(f"Starting blog post creation for topic: {pen.yellow_bright(topic)}")
        draft = self.writer.write_content(topic)
        
        self.logger.log_block("SUBMITTED DRAFT", pen.gray(draft))
        
        self.logger.log("Draft created. Initiating review ...")
        result = self.editor.review_content(draft)
        self.logger.log_block("FEEDBACK", pen.gray(result["suggested_feedback"]))
        flawless = result["score"]['flawless']
        content_quality = result["score"]['average_score']
        self.logger.log(f"Writer received average score: {content_quality}")

        revision_round = 1
        while not flawless and revision_round <= review_limit:
            self.logger.log(f"Revision round {revision_round} ...")
            draft = self.writer.revise_content(result["overall_score"], result["suggested_feedback"])
            self.logger.log_block("RESUBMITTED DRAFT", pen.gray(draft))

            result = self.editor.review_content(draft)
            self.logger.log_block("FEEDBACK", pen.gray(result["suggested_feedback"]))
            
            flawless = result["score"]['flawless']
            content_quality = result["score"]['average_score']
            self.logger.log(f"Writer received average score: {content_quality}")
            revision_round += 1

        if content_quality < quality_threshold:
            self.logger.log(f"Warning: Final content quality score {content_quality} is below threshold {quality_threshold}.")
        else:
            self.logger.log("Blog post creation completed and approved!")
            metadata = self.seo.create_metadata(draft)
            self.publisher.publish(draft, metadata)
        return draft
