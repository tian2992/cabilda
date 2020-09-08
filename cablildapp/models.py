#models
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, Text, JSON
from database import Base
import datetime

# https://github.com/edkrueger/sars-flask/blob/master/app/models.py

class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


class User(Base, DictMixIn):
    __tablename__ = "Userz"
    # a phonenumber
    user_id = Column(String(64), primary_key=True, index=True)
    country = Column(String(2), nullable=True)
    answers = relationship("Answer", backref="user")


class Question(Base, DictMixIn):
    __tablename__ = "Question"

    block_id = Column(String(8), primary_key=True, index=True)
    cat = Column(String(4))
    desc = Column(Text, index=True)
    answers = relationship("Answer", backref="question")


class Answer(Base, DictMixIn):
    __tablename__ = "Answer"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('Userz.user_id'))
    question_block_id = Column(String, ForeignKey('Question.block_id'))
    answer_data = Column(JSON)
    media_url = Column(String(250))


class Message(Base, DictMixIn):
    __tablename__ = "Message"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('Userz.user_id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    all_message = Column(JSON)
