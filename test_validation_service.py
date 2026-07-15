import os

from dotenv import load_dotenv


load_dotenv()

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "startup_validator.settings",
)

import django

django.setup()


from validator.services.validation_service import ValidationService


def main():
    service = ValidationService()

    report = service.validate_startup(
        title="AI Study Assistant",
        idea="""
        An AI platform for university students that uploads lectures,
        summarizes lecture content, and generates quizzes for students.
        """,
    )

    print("\n===== VALIDATION SAVED =====\n")

    print("Startup ID:")
    print(report.startup.id)

    print("\nStartup Title:")
    print(report.startup.title)

    print("\nBusiness Score:")
    print(report.business_analysis["business_score"])

    print("\nMarket Score:")
    print(report.market_analysis["market_score"])

    print("\nRisk Score:")
    print(report.risk_analysis["risk_score"])

    print("\nFinal Score:")
    print(report.score)

    print("\nRecommendation:")
    print(report.final_report["recommendation"])

    print("\nReport ID:")
    print(report.id)


if __name__ == "__main__":
    main()