from dotenv import load_dotenv

from validator.agents.risk_agent import RiskAgent


load_dotenv()


def main():
    agent = RiskAgent()

    idea = """
    An AI platform for university students that uploads lectures,
    summarizes lecture content, and generates quizzes for students.
    """

    result = agent.analyze(idea)

    print("\n===== RISK ANALYSIS =====\n")

    print("Business Risks:")
    for risk in result["business_risks"]:
        print(f"- {risk}")

    print("\nMarket Risks:")
    for risk in result["market_risks"]:
        print(f"- {risk}")

    print("\nOperational Risks:")
    for risk in result["operational_risks"]:
        print(f"- {risk}")

    print("\nTechnology Risks:")
    for risk in result["technology_risks"]:
        print(f"- {risk}")

    print("\nLegal and Privacy Risks:")
    for risk in result["legal_privacy_risks"]:
        print(f"- {risk}")

    print("\nFailure Scenarios:")
    for scenario in result["failure_scenarios"]:
        print(f"- {scenario}")

    print("\nRisk Level:")
    print(result["risk_level"])

    print("\nRisk Score:")
    print(result["risk_score"])

    print("\nPython Type:")
    print(type(result))


if __name__ == "__main__":
    main()