import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from app.ai.classifier import classify_conversation
from app.ai.responder import generate_veterinary_response
from app.ai.topic_classifier import classify_topic
from app.config.settings import TELEGRAM_BOT_TOKEN
from app.services.topic_service import TopicService


bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
)

dispatcher = Dispatcher()

topic_service = TopicService()


@dispatcher.message()
async def handle_message(
    message: Message,
) -> None:
    if not message.text:
        return

    chat_id = message.chat.id

    user_name = (
        message.from_user.full_name
        if message.from_user
        else "Unknown"
    )

    print()
    print("=" * 60)
    print("NEW TELEGRAM MESSAGE")
    print("=" * 60)

    print(f"Chat ID: {chat_id}")
    print(f"User: {user_name}")
    print(f"Text: {message.text}")

    active_topics = topic_service.get_active_topics(
        chat_id
    )

    active_topics_context = "\n\n".join(
        (
            f"Topic ID: {topic.topic_id}\n"
            f"Summary: {topic.summary}\n"
            f"Participants: "
            f"{', '.join(topic.participants)}"
        )
        for topic in active_topics
    )

    if not active_topics_context:
        active_topics_context = "There are no active topics."

    print()
    print("ACTIVE TOPICS:")
    print("-" * 60)
    print(active_topics_context)

    print()
    print("TOPIC CLASSIFICATION:")
    print("-" * 60)

    topic_classification = await classify_topic(
        new_message=message.text,
        active_topics=active_topics_context,
    )

    print(topic_classification)

    topic_type = topic_classification["topic_type"]

    if topic_type == "non_veterinary":
        print()
        print("Message is non-veterinary.")
        print("No action taken.")

        print("=" * 60)
        print()

        return

    if topic_type == "new_topic":
        topic = topic_service.create_topic(
            chat_id=chat_id,
            summary=message.text,
            user_name=user_name,
            message_text=message.text,
        )

    elif topic_type == "follow_up":
        topic_id = topic_classification["topic_id"]

        if topic_id is None:
            raise RuntimeError(
                "Topic classifier returned follow_up "
                "without a topic_id"
            )

        topic = topic_service.add_message_to_topic(
            chat_id=chat_id,
            topic_id=topic_id,
            user_name=user_name,
            message_text=message.text,
        )

    else:
        raise RuntimeError(
            f"Unknown topic type: {topic_type}"
        )

    conversation_context = "\n".join(
        f"{item['user']}: {item['text']}"
        for item in topic.messages
    )

    print()
    print("SELECTED TOPIC:")
    print("-" * 60)
    print(f"Topic ID: {topic.topic_id}")
    print(f"Topic Summary: {topic.summary}")

    print()
    print("TOPIC CONVERSATION CONTEXT:")
    print("-" * 60)
    print(conversation_context)

    print()
    print("AI CLASSIFICATION:")
    print("-" * 60)

    classification = await classify_conversation(
        conversation_context
    )

    print(classification)

    if classification["should_respond"]:
        veterinary_response = await generate_veterinary_response(
            conversation_context,
            classification,
        )

        print()
        print("AI VETERINARY RESPONSE:")
        print("-" * 60)
        print(veterinary_response)

        await message.answer(
            veterinary_response
        )

    print("=" * 60)
    print()


async def main() -> None:
    print(
        "Vet AI Telegram Bot is starting..."
    )

    await dispatcher.start_polling(
        bot
    )


if __name__ == "__main__":
    asyncio.run(main())