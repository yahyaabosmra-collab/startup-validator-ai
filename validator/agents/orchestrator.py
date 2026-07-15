# from validator.agents.business_agent import BusinessAgent
# from validator.agents.market_agent import MarketAgent
# from validator.agents.risk_agent import RiskAgent
# from validator.agents.report_agent import ReportAgent
# from validator.services.score_calculator import ScoreCalculator


# class StartupAnalysisOrchestrator:

#     def __init__(self):
#         self.business_agent = BusinessAgent()
#         self.market_agent = MarketAgent()
#         self.risk_agent = RiskAgent()
#         self.report_agent = ReportAgent()

#     def analyze(self, idea: str) -> dict:
#         business_analysis = self.business_agent.analyze(idea)

#         market_analysis = self.market_agent.analyze(idea)

#         risk_analysis = self.risk_agent.analyze(idea)
#         print(
#     "RISK BREAKDOWN:",
#     risk_analysis["score_breakdown"],
#      )
#         final_score = ScoreCalculator.calculate(
#             business_score=business_analysis["business_score"],
#             market_score=market_analysis["market_score"],
#             risk_score=risk_analysis["risk_score"],
#         )

#         final_report = self.report_agent.generate_report(
#             business_analysis=business_analysis,
#             market_analysis=market_analysis,
#             risk_analysis=risk_analysis,
#             final_score=final_score,
#         )

#         return {
#             "business_analysis": business_analysis,
#             "market_analysis": market_analysis,
#             "risk_analysis": risk_analysis,
#             "final_score": final_score,
#             "final_report": final_report,
#         }









from validator.agents.business_agent import BusinessAgent
from validator.agents.market_agent import MarketAgent
from validator.agents.risk_agent import RiskAgent
from validator.agents.report_agent import ReportAgent
from validator.services.score_calculator import ScoreCalculator


class StartupAnalysisOrchestrator:

    def __init__(self):
        self.business_agent = BusinessAgent()
        self.market_agent = MarketAgent()
        self.risk_agent = RiskAgent()
        self.report_agent = ReportAgent()

    def analyze(self, idea: str) -> dict:
        business_analysis = self.business_agent.analyze(idea)

        market_analysis = self.market_agent.analyze(idea)

        risk_analysis = self.risk_agent.analyze(idea)

        final_score = ScoreCalculator.calculate(
            business_score=business_analysis["business_score"],
            market_score=market_analysis["market_score"],
            risk_score=risk_analysis["risk_score"],
        )

        final_verdict = ScoreCalculator.get_verdict(
            final_score
        )

        final_report = self.report_agent.generate_report(
            business_analysis=business_analysis,
            market_analysis=market_analysis,
            risk_analysis=risk_analysis,
            final_score=final_score,
        )

        return {
            "business_analysis": business_analysis,
            "market_analysis": market_analysis,
            "risk_analysis": risk_analysis,
            "final_score": final_score,
            "final_verdict": final_verdict,
            "final_report": final_report,
        }