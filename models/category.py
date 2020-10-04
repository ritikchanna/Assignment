from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, relation
from db import Base
from models.subject import Subject
import json

category_subject_association = Table(
    'category_subject', Base.metadata,
    Column('category_id', Integer, ForeignKey("categories.id")),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)


class Category(Base):
    __tablename__ = 'categories'
    id = Column('id', Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    parent = relationship('Category', remote_side=[id],backref="sub_categories")
    name = Column('name', String(32))
    subjects = relationship("Subject", secondary=category_subject_association)

    def __init__(self, name):
        self.name = name

    def get_children(self):
        return self.subjects if len(self.subjects) > 0 else self.sub_categories

    def append_child(self, children):
        if type(children) == Category:
            if len(self.subjects) > 1:
                raise Exception("Invalid Child type[Category] for this category")
            else:
                self.sub_categories.append(children)
        elif type(children) == Subject:
            if len(self.sub_categories) > 1:
                raise Exception("Invalid Child type[Subject] for this category")
            else:
                self.subjects.append(children)
        else:
            raise Exception("Invalid Child type for exam")

    def json(self):
        child_json = "[ "
        if self.get_children() is not None:
            for child in self.get_children():
                child_json += json.dumps(child.json()) + ","
        child_json = child_json[:-1] + "]"
        return {
            "id": self.id,
            "name": self.name,
            ("subjects" if len(self.subjects) > 0 else "categories"): json.loads(child_json)
        }
