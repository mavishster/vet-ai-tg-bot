import asyncio

from classifier import classify_conversation
from responder import generate_veterinary_response


async def main():
    conversation_context = """
    @ms: Моя собака со вчерашнего дня постоянно рвёт, она очень слабая и не хочет пить воду.
    """

    classification = await classify_conversation(
        conversation_context
    )

    print("Classification result:")
    print(classification)

    print()
    print("Veterinary response:")
    print("-" * 60)

    response = await generate_veterinary_response(
        conversation_context,
        classification,
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())