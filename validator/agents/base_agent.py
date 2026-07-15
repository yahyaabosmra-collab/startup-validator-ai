from abc import ABC, abstractmethod


class BaseAgent(ABC):

    @abstractmethod
    def analyze(self, idea: str) -> str:
        pass