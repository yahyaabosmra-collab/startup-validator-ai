class ScoreCalculator:

    BUSINESS_WEIGHT = 0.40
    MARKET_WEIGHT = 0.35
    RISK_WEIGHT = 0.25

    @classmethod
    def calculate(
        cls,
        business_score: float,
        market_score: float,
        risk_score: float,
    ) -> float:

        business_score = cls._validate_score(
            business_score,
            "business_score",
        )

        market_score = cls._validate_score(
            market_score,
            "market_score",
        )

        risk_score = cls._validate_score(
            risk_score,
            "risk_score",
        )

        risk_potential_score = 10 - risk_score

        final_score = (
            business_score * cls.BUSINESS_WEIGHT
            + market_score * cls.MARKET_WEIGHT
            + risk_potential_score * cls.RISK_WEIGHT
        )

        return round(final_score, 2)

    @staticmethod
    def get_verdict(final_score: float) -> str:
        final_score = ScoreCalculator._validate_score(
            final_score,
            "final_score",
        )

        if final_score < 4:
            return "Weak Potential"

        if final_score < 6.5:
            return "Moderate Potential"

        if final_score < 8:
            return "Good Potential"

        return "Strong Potential"

    @staticmethod
    def _validate_score(score: float, name: str) -> float:
        try:
            score = float(score)

        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"{name} must be a number"
            ) from exc

        if not 0 <= score <= 10:
            raise ValueError(
                f"{name} must be between 0 and 10"
            )

        return score