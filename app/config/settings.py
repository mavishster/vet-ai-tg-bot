import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured"
    )

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN is not configured"
    )

GEMINI_TOPIC_CLASSIFIER_MODEL = "gemini-3.5-flash-lite"

GEMINI_CONVERSATION_CLASSIFIER_MODEL = "gemini-3.5-flash-lite"

GEMINI_VETERINARY_RESPONSE_MODEL = "gemini-3.5-flash"