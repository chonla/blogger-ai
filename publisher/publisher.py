from abc import abstractmethod
from typing import Dict


class Publisher:
    @abstractmethod
    def publish(self, content: str, metadata: Dict):
        pass
    
    @abstractmethod
    def name(self) -> str:
        pass