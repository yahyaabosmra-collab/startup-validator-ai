from validator.services.score_calculator import ScoreCalculator


def main():
    final_score = ScoreCalculator.calculate(
        business_score=7.5,
        market_score=7.0,
        risk_score=8.0,
    )

    print("\n===== SCORE CALCULATION =====\n")
    print(f"Final Score: {final_score}")


if __name__ == "__main__":
    main()