import json

from validator.agents.base_agent import BaseAgent
from validator.services.huggingface import HuggingFaceService
from validator.services.prompt_loader import load_prompt


class RiskAgent(BaseAgent):

    def __init__(self):
        self.llm = HuggingFaceService()
        self.instructions = load_prompt("risk.txt")

    def analyze(self, idea: str) -> dict:
        prompt = f"""
{self.instructions}

Startup Idea:
{idea}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "RiskAgent returned invalid JSON"
            ) from exc