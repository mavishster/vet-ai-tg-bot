import json

from app.config.settings import GEMINI_CONVERSATION_CLASSIFIER_MODEL
from app.services.gemini_service import GeminiService


gemini_service = GeminiService()


CLASSIFIER_SYSTEM_PROMPT = """
Classify the LAST message in a Telegram conversation about pets and veterinary topics.

Use previous messages only as context.

Return JSON only:
{
    "should_respond": boolean,
    "category": string,
    "priority": string,
    "reason": string
}

Categories:
- casual: greetings and normal small talk
- personal_experience: sharing a pet experience without asking for help
- veterinary_question: general veterinary or pet-care question
- professional_opinion: asking for veterinary guidance or professional opinion
- potentially_dangerous_advice: unsafe treatment or medication advice
- urgent_veterinary_situation: potentially serious symptoms requiring prompt veterinary care
- non_veterinary: unrelated to pets or veterinary topics

Priority:
- none: no response needed
- normal: ordinary veterinary information
- high: dangerous advice or urgent situation

Respond when the latest message needs useful veterinary information,
safety guidance, or urgent advice.

Always classify the LAST message, not an earlier message.
Return valid JSON only.
"""


async def classify_conversation(
    conversation_context: str,
) -> dict:
    prompt = (
        f"{CLASSIFIER_SYSTEM_PROMPT}\n\n"
        "CONVERSATION CONTEXT:\n"
        f"{conversation_context}"
    )

    response_content = await gemini_service.generate(
        model=GEMINI_CONVERSATION_CLASSIFIER_MODEL,
        prompt=prompt,
        response_mime_type="application/json",
    )

    return json.loads(response_content)