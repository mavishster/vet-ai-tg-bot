import asyncio

from app.ai.topic_classifier import classify_topic


async def main():
    test_cases = [
        (
            "TEST 1 - New veterinary topic",
            """
            There are no active topics.
            """,
            "My dog has been vomiting since yesterday.",
        ),
        (
            "TEST 2 - Follow-up to existing topic",
            """
            Topic ID: 1
            Summary: @ms is discussing a dog that has been vomiting since yesterday.
            Participants: @ms
            """,
            "She still isn't drinking water.",
        ),
    ]

    for test_name, active_topics, new_message in test_cases:
        print()
        print("=" * 60)
        print(test_name)
        print("=" * 60)

        print("ACTIVE TOPICS:")
        print(active_topics.strip())

        print()
        print("NEW MESSAGE:")
        print(new_message)

        print()
        print("CLASSIFICATION:")

        result = await classify_topic(
            new_message=new_message,
            active_topics=active_topics.strip(),
        )

        print(result)


if __name__ == "__main__":
    asyncio.run(main())