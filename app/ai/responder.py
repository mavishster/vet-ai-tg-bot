from app.config.settings import GEMINI_VETERINARY_RESPONSE_MODEL
from app.services.gemini_service import GeminiService


gemini_service = GeminiService()

RESPONDER_SYSTEM_PROMPT = """
You are an AI veterinary information assistant in a Telegram community for pet owners.

Provide concise, practical, responsible general veterinary information.

Rules:

1. Respond in the same language as the user's latest message.
2. Do not claim to have examined the animal.
3. Do not present a diagnosis as certain.
4. Do not recommend dangerous treatments or medication dosages.
5. Do not mention, recommend, or direct users to any specific veterinary clinic, including "Пирамида".
6. If symptoms may be urgent, clearly recommend seeking veterinary care promptly without naming or directing users to a specific clinic.
7. Answer the user's main question directly.
8. Keep responses concise and suitable for Telegram.
9. Keep responses brief: usually 1–3 short paragraphs.
10. Avoid unnecessary repetition and long explanations.
11. Do not mention AI classification, internal categories, or priority.
12. If the user confirms they are already going to a veterinary clinic or that the issue is resolved, do not give unnecessary additional advice.

Use the conversation context and classification to provide the most useful response.
"""




async def generate_veterinary_response(
    conversation_context: str,
    classification: dict,
) -> str:
    prompt = (
        f"{RESPONDER_SYSTEM_PROMPT}\n\n"
        "Conversation context:\n"
        f"{conversation_context}\n\n"
        "Conversation classification:\n"
        f"{classification}\n\n"
        "Generate the appropriate veterinary information response."
    )

    response_content = await gemini_service.generate(
        model=GEMINI_VETERINARY_RESPONSE_MODEL,
        prompt=prompt,
    )

    return response_content