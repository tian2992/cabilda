#models
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
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


class Record(Base, DictMixIn):
    __tablename__ = "Records"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    country = Column(String, index=True)
    cases = Column(Integer)
    deaths = Column(Integer)
    recoveries = Column(Integer)
