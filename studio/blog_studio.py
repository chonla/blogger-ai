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
        candidate = None

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
        
        self.logger.debug_block("SUBMITTED DRAFT", draft)
        
        self.logger.log("Draft created. Initiating review ...")
        result = self.editor.review_content(draft)
        self.logger.debug_block("FEEDBACK", result["suggested_feedback"])
        flawless = result["score"]['flawless']
        content_quality = result["score"]['average_score']
        self.logger.log(f"Writer received average score: {content_quality}")

        if content_quality >= quality_threshold or flawless:
            candidate = {
                "content": draft,
                "score": content_quality,
                "flawless": flawless
            }

        revision_round = 1
        while not flawless and revision_round <= review_limit:
            self.logger.log(f"Revision round {revision_round} ...")
            draft = self.writer.revise_content(result["overall_score"], result["suggested_feedback"])
            self.logger.debug_block("RESUBMITTED DRAFT", draft)

            result = self.editor.review_content(draft)
            self.logger.debug_block("FEEDBACK", result["suggested_feedback"])
            
            flawless = result["score"]['flawless']
            content_quality = result["score"]['average_score']
            self.logger.log(f"Writer received average score: {content_quality}")
            
            if content_quality >= quality_threshold or flawless:
                if candidate is None:
                    candidate = {
                        "content": draft,
                        "score": content_quality,
                        "flawless": flawless
                    }
                else:
                    # Keep the best candidate
                    if content_quality > candidate["score"]:
                        candidate = {
                            "content": draft,
                            "score": content_quality,
                            "flawless": flawless
                        }
            revision_round += 1

        if candidate is not None:
            draft = candidate["content"]
            content_quality = candidate["score"]
            flawless = candidate["flawless"]
            if flawless:
                self.logger.log(f"Content automatically approved with flawless score! Awesome job!")
            else:
                self.logger.log(f"Content automatically approved with score below flawless threshold.")
            metadata = self.seo.create_metadata(draft)
            self.publisher.publish(draft, metadata)
        else:
            self.logger.log("Failed to produce acceptable content within the review limit.")
        return candidate
