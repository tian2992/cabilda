#models
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date, Text, JSON
from .database import Base
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


class Questions(Base, DictMixIn):
    __tablename__ = "Questions"

    block_id = Column(String(8), primary_key=True, index=True)
    cat = Column(String(4))
    desc = Column(Text, index=True)
    
    answers = relationship("Answers", backref="question")

    
class Answers(Base, DictMixIn):
    id = Column(Integer, primary_key=True, index=True)
    
    question_block_id = Column(String, ForeignKey('Questions.block_id'))
    answer_data = Column(JSON)
    url_data = Column(String(250))
    

    
