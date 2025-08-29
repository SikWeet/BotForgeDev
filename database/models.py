from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	telegram_id = Column(Integer, unique=True, index=True)
	first_name = Column(String)
	last_name = Column(String)
	username = Column(String)

	bots = relationship("Bot", back_populates="owner")


class Bot(Base):
	__tablename__ = "bots"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	bot_token = Column(String)
	bot_name = Column(String)

	owner = relationship("User", back_populates="bots")
	features = relationship("BotFeature", back_populates="bot")
	message_templates = relationship("BotMessageTemplate", back_populates="bot")


class BotFeature(Base):
	__tablename__ = "bot_features"
	id = Column(Integer, primary_key=True, index=True)
	bot_id = Column(Integer, ForeignKey("bots.id"))
	feature_name = Column(String)
	enabled = Column(Boolean, default=False)

	bot = relationship("Bot", back_populates="features")


class BotMessageTemplate(Base):
	__tablename__ = "bot_message_templates"
	id = Column(Integer, primary_key=True, index=True)
	bot_id = Column(Integer, ForeignKey("bots.id"))
	feature_name = Column(String)
	template_text = Column(Text)

	bot = relationship("Bot", back_populates="message_templates")
