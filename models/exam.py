from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models.subject import Subject
from models.category import Category
import json

exam_category_association = Table(
    'exam_category', Base.metadata,
    Column('exam_id', Integer, ForeignKey('exams.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)
exam_subject_association = Table(
    'exam_subject', Base.metadata,
    Column('exam_id', Integer, ForeignKey('exams.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)


class Exam(Base):
    __tablename__ = 'exams'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(32))
    categories = relationship("Category", secondary=exam_category_association)
    subjects = relationship("Subject", secondary=exam_subject_association)

    def __init__(self, name):
        self.name = name

    def get_children(self):
        return self.subjects if len(self.subjects) > 0 else self.categories

    def append_child(self, children):
        if type(children) == Category:
            if len(self.subjects) > 1:
                raise HTTPException(status_code=400, detail="Invalid Child type[Category] for this exam")
            else:
                self.categories.append(children)
        elif type(children) == Subject:
            if len(self.categories) > 1:
                raise HTTPException(status_code=400, detail="Invalid Child type[Subject] for this exam")
            else:
                self.subjects.append(children)
        else:
            raise HTTPException(status_code=400, detail="Invalid Child type for exam")

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
