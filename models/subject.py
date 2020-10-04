from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models.topic import Topic
import json

subject_topic_association = Table(
    'subject_topic', Base.metadata,
    Column('subject_id', Integer, ForeignKey("subjects.id")),
    Column('topic_id', Integer, ForeignKey('topics.id'))
)


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(32))
    topics = relationship("Topic", secondary=subject_topic_association)

    def __init__(self, name):
        self.name = name

    def get_children(self):
        return self.topics

    def append_child(self, children):
        if type(children) == Topic:
            self.topics.append(children)
        else:
            raise HTTPException(status_code=400, detail="Invalid Child type for Subject")

    def json(self):
        child_json = "[ "
        if self.get_children() is not None:
            for child in self.get_children():
                child_json += json.dumps(child.json()) + ","
        child_json = child_json[:-1] + "]"
        return {
            "id": self.id,
            "name": self.name,
            "topics": json.loads(child_json)
        }
