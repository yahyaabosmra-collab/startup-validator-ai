import os
import time

from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError


class HuggingFaceService:
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2

    def __init__(self):
        self.token = os.getenv("HF_TOKEN")

        if not self.token:
            raise ValueError("HF_TOKEN is not configured")

        self.model = "Qwen/Qwen3-8B"

        self.client = InferenceClient(
            provider="nscale",
            api_key=self.token,
        )

    def generate(self, prompt: str) -> str:
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    max_tokens=2000,
                    temperature=0.7,
                )

                content = response.choices[0].message.content

                if not content:
                    raise ValueError(
                        "Hugging Face returned an empty response"
                    )

                return content

            except HfHubHTTPError as exc:
                status_code = (
                    exc.response.status_code
                    if exc.response is not None
                    else None
                )

                is_server_error = (
                    status_code is not None
                    and 500 <= status_code < 600
                )

                if not is_server_error:
                    raise

                if attempt == self.MAX_RETRIES:
                    raise RuntimeError(
                        "Hugging Face inference failed "
                        f"after {self.MAX_RETRIES} attempts"
                    ) from exc

                print(
                    f"Hugging Face server error "
                    f"({status_code}). "
                    f"Retrying {attempt}/{self.MAX_RETRIES}..."
                )

                time.sleep(self.RETRY_DELAY_SECONDS)

        raise RuntimeError(
            "Unexpected Hugging Face inference failure"
        )