import os

from dotenv import load_dotenv

from validator.services.huggingface import HuggingFaceService


load_dotenv()


def main():
    llm = HuggingFaceService()

    response = llm.generate(
        "What is a startup? Answer in one short paragraph."
    )

    print(response)


if __name__ == "__main__":
    main()