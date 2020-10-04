from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, relation
from db import Base
import json


class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('topics.id'))
    parent = relationship('Topic', remote_side=[id], backref="sub_topics")
    name = Column('name', String(32))

    def __init__(self, name):
        self.name = name

    def get_children(self):
        return self.sub_topics

    def append_child(self, children):
        if type(children) == Topic:

            self.sub_topics.append(children)
        else:
            raise Exception("Invalid Child type for Topic")

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
