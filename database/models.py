from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

base = declarative_base()

class StreamerModel(Base):
    __tablename__ = "streamer"
    id = Column(
        'id',
        Integer,
        primary_key=True
    )
    