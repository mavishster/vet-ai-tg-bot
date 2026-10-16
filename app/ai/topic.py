from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConversationTopic:
    topic_id: int
    summary: str
    participants: set[str] = field(default_factory=set)
    messages: list[dict[str, str]] = field(default_factory=list)
    last_activity: datetime | None = None