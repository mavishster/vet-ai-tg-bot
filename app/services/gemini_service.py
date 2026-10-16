import asyncio

from google import genai
from google.genai import errors, types

from app.config.settings import GEMINI_API_KEY


class GeminiService:
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
        )

    async def generate(
        self,
        model: str,
        prompt: str,
        response_mime_type: str | None = None,
    ) -> str:
        for attempt in range(self.MAX_RETRIES):
            try:
                config = None

                if response_mime_type:
                    config = types.GenerateContentConfig(
                        response_mime_type=response_mime_type,
                    )

                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=model,
                    contents=prompt,
                    config=config,
                )

                response_content = response.text

                if not response_content:
                    raise RuntimeError(
                        "Gemini returned an empty response"
                    )

                return response_content

            except errors.ClientError as exception:
                if exception.code == 429:
                    raise RuntimeError(
                        "Gemini API quota or rate limit exceeded. "
                        "Please wait or check your Gemini API quota."
                    ) from exception

                raise

            except errors.ServerError:
                if attempt == self.MAX_RETRIES - 1:
                    raise

                await asyncio.sleep(
                    self.RETRY_DELAY_SECONDS
                )

        raise RuntimeError(
            "Gemini request failed after maximum retries"
        )