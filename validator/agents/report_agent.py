import json

from validator.agents.base_agent import BaseAgent
from validator.services.huggingface import HuggingFaceService
from validator.services.prompt_loader import load_prompt


class ReportAgent(BaseAgent):

    def __init__(self):
        self.llm = HuggingFaceService()
        self.instructions = load_prompt("report.txt")

    def analyze(self, idea: str) -> dict:
        raise NotImplementedError(
            "ReportAgent requires structured agent analyses."
        )

    def generate_report(
        self,
        business_analysis: dict,
        market_analysis: dict,
        risk_analysis: dict,
        final_score: float,
    ) -> dict:

        prompt = f"""
{self.instructions}

BUSINESS ANALYSIS:
{json.dumps(business_analysis, ensure_ascii=False)}

MARKET ANALYSIS:
{json.dumps(market_analysis, ensure_ascii=False)}

RISK ANALYSIS:
{json.dumps(risk_analysis, ensure_ascii=False)}

FINAL SCORE:
{final_score}
"""

        response = self.llm.generate(prompt)

        try:
            report = json.loads(response)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "ReportAgent returned invalid JSON"
            ) from exc

        return report