from dotenv import load_dotenv

from validator.agents.business_agent import BusinessAgent


load_dotenv()


def main():
    agent = BusinessAgent()

    idea = """
    An AI platform for university students that uploads lectures,
    summarizes lecture content, and generates quizzes for students.
    """

    result = agent.analyze(idea)

    print("\n===== BUSINESS ANALYSIS =====\n")

    print("Problem:")
    print(result["problem"])

    print("\nTarget Audience:")
    print(result["target_audience"])

    print("\nValue Proposition:")
    print(result["value_proposition"])

    print("\nStrengths:")
    for strength in result["strengths"]:
        print(f"- {strength}")

    print("\nWeaknesses:")
    for weakness in result["weaknesses"]:
        print(f"- {weakness}")

    print("\nBusiness Score:")
    print(result["business_score"])

    print("\nPython Type:")
    print(type(result))


if __name__ == "__main__":
    main()