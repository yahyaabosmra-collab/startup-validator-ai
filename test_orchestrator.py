from dotenv import load_dotenv

from validator.agents.orchestrator import StartupAnalysisOrchestrator


load_dotenv()


def main():
    orchestrator = StartupAnalysisOrchestrator()

    idea = """
    An AI platform for university students that uploads lectures,
    summarizes lecture content, and generates quizzes for students.
    """

    print("\nStarting startup analysis...\n")

    result = orchestrator.analyze(idea)

    print("\n===== AGENT SCORES =====\n")

    print(
        "Business Score:",
        result["business_analysis"]["business_score"],
    )

    print(
        "Market Score:",
        result["market_analysis"]["market_score"],
    )

    print(
        "Risk Score:",
        result["risk_analysis"]["risk_score"],
    )

    print("\n===== FINAL SCORE =====\n")
    print(result["final_score"])

    print("\n===== FINAL REPORT =====\n")

    report = result["final_report"]

    print("Executive Summary:")
    print(report["executive_summary"])

    print("\nBusiness Evaluation:")
    print(report["business_evaluation"])

    print("\nMarket Evaluation:")
    print(report["market_evaluation"])

    print("\nRisk Evaluation:")
    print(report["risk_evaluation"])

    print("\nKey Strengths:")
    for strength in report["key_strengths"]:
        print(f"- {strength}")

    print("\nKey Concerns:")
    for concern in report["key_concerns"]:
        print(f"- {concern}")

    print("\nOverall Score:")
    print(report["overall_score"])

    print("\nRecommendation:")
    print(report["recommendation"])

    print("\nRecommendation Reason:")
    print(report["recommendation_reason"])

    print("\nFinal Report Type:")
    print(type(report))


if __name__ == "__main__":
    main()