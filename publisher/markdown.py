from typing import Dict
from logger.logger import Logger
from pen.pen import pen


class MarkdownPublisher:
    def __init__(self):
        self.logger = Logger("publisher", pen.magenta_bright)
    
    def publish(self, content: str, metadata: Dict):
        file_path = metadata.get("suggested_url_slug", "blog_post").replace(" ", "_") + ".md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.logger.log(f"Content published to {pen.yellow_bright(file_path)}")