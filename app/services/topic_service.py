from datetime import datetime

from app.ai.topic import ConversationTopic


class TopicService:
    def __init__(self) -> None:
        self.topics: dict[
            int,
            dict[int, ConversationTopic],
        ] = {}

        self.next_topic_ids: dict[int, int] = {}

    def create_topic(
        self,
        chat_id: int,
        summary: str,
        user_name: str,
        message_text: str,
    ) -> ConversationTopic:
        if chat_id not in self.topics:
            self.topics[chat_id] = {}

        if chat_id not in self.next_topic_ids:
            self.next_topic_ids[chat_id] = 1

        topic = ConversationTopic(
            topic_id=self.next_topic_ids[chat_id],
            summary=summary,
            participants={user_name},
            messages=[
                {
                    "user": user_name,
                    "text": message_text,
                }
            ],
            last_activity=datetime.now(),
        )

        self.topics[chat_id][topic.topic_id] = topic

        self.next_topic_ids[chat_id] += 1

        return topic

    def get_topic(
        self,
        chat_id: int,
        topic_id: int,
    ) -> ConversationTopic | None:
        chat_topics = self.topics.get(
            chat_id,
            {},
        )

        return chat_topics.get(topic_id)

    def get_active_topics(
        self,
        chat_id: int,
    ) -> list[ConversationTopic]:
        chat_topics = self.topics.get(
            chat_id,
            {},
        )

        return list(
            chat_topics.values()
        )

    def add_message_to_topic(
        self,
        chat_id: int,
        topic_id: int,
        user_name: str,
        message_text: str,
    ) -> ConversationTopic:
        topic = self.get_topic(
            chat_id=chat_id,
            topic_id=topic_id,
        )

        if topic is None:
            raise ValueError(
                f"Topic with ID {topic_id} "
                f"does not exist in chat {chat_id}"
            )

        topic.participants.add(
            user_name
        )

        topic.messages.append(
            {
                "user": user_name,
                "text": message_text,
            }
        )

        topic.last_activity = datetime.now()

        return topic