from dotenv import load_dotenv

from validator.agents.market_agent import MarketAgent


load_dotenv()


def main():
    agent = MarketAgent()

    idea = """
    An AI platform for university students that uploads lectures,
    summarizes lecture content, and generates quizzes for students.
    """

    result = agent.analyze(idea)

    print("\n===== MARKET ANALYSIS =====\n")

    print("Market Need:")
    print(result["market_need"])

    print("\nCustomer Demand:")
    print(result["customer_demand"])

    print("\nCompetition Level:")
    print(result["competition_level"])

    print("\nCompetitor Types:")
    for competitor in result["competitor_types"]:
        print(f"- {competitor}")

    print("\nOpportunities:")
    for opportunity in result["opportunities"]:
        print(f"- {opportunity}")

    print("\nChallenges:")
    for challenge in result["challenges"]:
        print(f"- {challenge}")

    print("\nMarket Score:")
    print(result["market_score"])

    print("\nPython Type:")
    print(type(result))


if __name__ == "__main__":
    main()