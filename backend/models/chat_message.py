from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # "user" | "assistant"
    role = Column(String(20), nullable=False, index=True)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
