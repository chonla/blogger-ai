from typing import Dict
from logger.logger import Logger
from pen.pen import pen
from .publisher import Publisher


class ScreenPublisher(Publisher):
    def __init__(self):
        self.logger = Logger("publisher", pen.magenta_bright)

    def name(self) -> str:
        return "screen publisher"

    def publish(self, content: str, metadata: Dict):
        self.logger.log(f"publishing with {pen.yellow_bright(self.name())}")
        self.logger.log_block("PUBLISHED CONTENT", content)
