import json

from models.exam import Exam
from models.category import Category
from models.exam import Exam
from models.subject import Subject
from models.topic import Topic
from db import session_factory

from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/{node_type}")
async def create_exam(node_type: str, name: str = Form(...)):
    klass = globals()[node_type]
    instance = klass(name)
    session = session_factory()
    session.add(instance)
    session.commit()
    return {"id": instance.id, "name": instance.name}


@app.post("/{node_type}/{path}")
async def create_node(node_type: str, path: str, name: str = Form(...), child_node_type: str = Form(...)):
    session = session_factory()
    klass = globals()[node_type]
    path_tokens = path.split('/')
    node = session.query(klass).get(path_tokens[0])
    leaf_node = get_node(node, path_tokens[1:])
    print(child_node_type)
    klass2 = globals()[child_node_type]
    new_node = klass2(name)
    leaf_node.append_child(new_node)
    session.commit()
    return new_node.id


@app.get("/{type}/{node_id}")
async def get_node(type, node_id):
    print(node_id)
    session = session_factory()
    klass = globals()[type]
    node = session.query(klass).get(node_id)
    session.close()
    return node


@app.get("/")
async def get_all():
    session = session_factory()
    exam_query = session.query(Exam)
    session.close()
    print(list_to_json(exam_query.all()))
    return list_to_json(exam_query.all())


@app.get("/exam")
async def get_all():
    session = session_factory()
    exam_query = session.query(Exam)
    session.close()
    return exam_query.all()


def list_to_json(exams_list):
    json_string = "["
    for item in exams_list:
        json_string += json.dumps(item.json()) + ","
    json_string = json_string[:-1] + "]"
    return json.loads(json_string)


def get_node(root, path_tokens):
    if len(path_tokens) < 1:
        return root
    for child_node in root.get_children():
        if child_node.name == path_tokens[0]:
            return get_node(child_node, path_tokens[1:])

    return None
