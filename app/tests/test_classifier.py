import asyncio

from app.ai.classifier import classify_conversation


async def main():
    test_conversations = [
        (
            "TEST 1 - Casual conversation",
            """
            @john: Good morning everyone!
            @mary: Good morning!
            @john: How are your pets doing today?
            """,
        ),
        (
            "TEST 2 - Personal experience",
            """
            @john: My cat was sick last month.
            @mary: Oh no, is she better now?
            @john: Yes, thankfully. The vet treated her and she recovered.
            """,
        ),
        (
            "TEST 3 - General veterinary question",
            """
            @john: Can dogs eat carrots?
            """,
        ),
        (
            "TEST 4 - Potentially dangerous advice",
            """
            @john: My dog has diarrhea.
            @mary: Just give him some human antibiotics. It worked for my dog.
            """,
        ),
        (
            "TEST 5 - Urgent veterinary situation",
            """
            @john: My dog has been vomiting all day and is extremely weak.
            He also cannot stand properly.
            """,
        ),
        (
            "TEST 6 - Russian veterinary question",
            """
            @ms: Можно ли кошкам давать молоко?
            """,
        ),
        (
            "TEST 7 - Non-veterinary conversation",
            """
            @john: Does anyone know a good restaurant nearby?
            @mary: Yes, there is a nice place downtown.
            """,
        ),
        (
            "TEST 8 - Follow-up question",
            """
            @ms: My dog has been vomiting since yesterday.
            AI: The dog should be examined by a veterinarian as soon as possible.
            @ms: What should I do right now?
            """,
        ),
        (
            "TEST 9 - New information",
            """
            @ms: My dog has been vomiting since yesterday.
            AI: The dog should be examined by a veterinarian as soon as possible.
            @ms: She still isn't drinking water.
            """,
        ),
        (
            "TEST 10 - Acknowledgement",
            """
            @ms: My dog has been vomiting since yesterday.
            AI: The dog should be examined by a veterinarian as soon as possible.
            @ms: Спасибо, мы уже едем в клинику.
            """,
        ),
    ]

    for test_name, conversation_context in test_conversations:
        print()
        print("=" * 60)
        print(test_name)
        print("=" * 60)

        result = await classify_conversation(
            conversation_context
        )

        print("Conversation:")
        print(conversation_context.strip())

        print()
        print("Classification:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())