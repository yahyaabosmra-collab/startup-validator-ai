from django.db import transaction

from validator.agents.orchestrator import StartupAnalysisOrchestrator
from validator.models import StartupIdea, ValidationReport


class ValidationService:

    def __init__(self):
        self.orchestrator = StartupAnalysisOrchestrator()

    @transaction.atomic
    def validate_startup(
        self,
        user,
        title: str,
        idea: str,
    ) -> ValidationReport:

        startup = StartupIdea.objects.create(
            user=user,
            title=title,
            idea=idea,
        )

        analysis_result = self.orchestrator.analyze(idea)

        report = ValidationReport.objects.create(
        startup=startup,
        business_analysis=analysis_result["business_analysis"],
        market_analysis=analysis_result["market_analysis"],
        risk_analysis=analysis_result["risk_analysis"],
        final_report=analysis_result["final_report"],
        score=analysis_result["final_score"],
        final_verdict=analysis_result["final_verdict"],
      )

        return report