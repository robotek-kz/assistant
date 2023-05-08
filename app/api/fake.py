import random
import click
import os
from dateutil import parser
import sqlite3
from flask import Blueprint
from faker import Faker
from api.app import db
from api.models import User, Post, TemplateSketch, ProjectGameSketch, FileGameSketch, TemplateFileSketch, TemplateProjectSketch,Level, GameSketch, \
    Files, Lines, LinesUserLink

fake = Blueprint('fake', __name__)
faker = Faker()

@fake.cli.command()
@click.argument('id', type=int)
def update_user_lines(id):
    line = db.session.query(LinesUserLink).filter_by(user_id = id, lines_id=8).one()
    line.state = 'init'
    line.current_char = 0
    line.current_line = 0
    db.session.add(line)
    db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def template(num):
    castle_defence = 'path'
    data = [
        {
            "name": "Castle Defense 1",
            "number": 1,
            "ext": "py",
            "mode": "python",
            "file_name": "step_1",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 17,
            "code": castle_defence + "step_1.py",
            "current": True,
            "score": 10,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_1.py",
            "previous_ready": "",
        },
        {
            "name": "Castle Defense 2",
            "number": 2,
            "ext": "py",
            "mode": "python",
            "file_name": "step_2",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 10,
            "code": castle_defence + "step_2.py",
            "current": False,
            "score": 10,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_2.py",
            "previous_ready": castle_defence + "ready_step_1.py",
        },
        {
            "name": "Castle Defense 3",
            "number": 3,
            "ext": "py",
            "mode": "python",
            "file_name": "step_3",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 31,
            "code": castle_defence + "step_3.py",
            "current": False,
            "score": 16,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_3.py",
            "previous_ready": castle_defence + "ready_step_2.py",
        },
        {
            "name": "Castle Defense 4",
            "number": 4,
            "ext": "py",
            "mode": "python",
            "file_name": "step_4",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 8,
            "code": castle_defence + "step_4.py",
            "score": 4,
            "current": False,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_4.py",
            "previous_ready": castle_defence + "ready_step_3.py",
        },
        {
            "name": "Castle Defense 5",
            "number": 5
            ,
            "ext": "py",
            "mode": "python",
            "file_name": "step_5",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 20,
            "code": castle_defence + "step_5.py",
            "score": 8,
            "current": False,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_5.py",
            "previous_ready": castle_defence + "ready_step_4.py",
        },
        {
            "name": "Castle Defense 6",
            "number": 6,
            "ext": "py",
            "mode": "python",
            "file_name": "step_6",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 33,
            "code": castle_defence + "step_6.py",
            "score": 15,
            "current": False,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_6.py",
            "previous_ready": castle_defence + "ready_step_5.py",
        },
        {
            "name": "Castle Defense 7",
            "number": 7,
            "ext": "py",
            "mode": "python",
            "file_name": "step_7",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 10,
            "code": castle_defence + "step_7.py",
            "score": 10,
            "current": False,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_7.py",
            "previous_ready": castle_defence + "ready_step_6.py",
        },
        {
            "name": "Castle Defense 8",
            "number": 8,
            "ext": "py",
            "mode": "python",
            "file_name": "step_8",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 12,
            "code": castle_defence + "step_8.py",
            "score": 4,
            "current": False,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_8.py",
            "previous_ready": castle_defence + "ready_step_7.py",
        },
        {
            "name": "Castle Defense 9",
            "number": 9,
            "ext": "py",
            "mode": "python",
            "file_name": "step_9",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 42,
            "code": castle_defence + "step_9.py",
            "score": 8,
            "current": False,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_9.py",
            "previous_ready": castle_defence + "ready_step_8.py",
        },
        {
            "name": "Castle Defense 10",
            "number": 10,
            "ext": "py",
            "mode": "python",
            "file_name": "step_10",
            "file_source": "https://www.kodeco.com/2795-beginning-game-programming-for-teens-with-python",
            "file_tab_size": 4,
            "file_lines": 15,
            "code": castle_defence + "step_10.py",
            "score": 5,
            "current": False,
            "difficulty": "hard",
            "ready": castle_defence + "ready_step_10.py",
            "previous_ready": castle_defence + "ready_step_9.py",
        }
    ]
    project_sketch = TemplateProjectSketch(name = 'Castle Defense')
    db.session.add(project_sketch)
    file_sketch = TemplateFileSketch(name = 'demo.py', template_project_sketches = project_sketch)
    db.session.add(file_sketch)
    lines = ''
    for i in data:
        file = i.get('code')
        with open(file) as f:
            lines = f.read()
        ready_file = i.get('ready')
        with open(ready_file) as f:
            ready_lines = f.read()
        previous_ready_file = i.get('previous_ready')
        if previous_ready_file == "":
            previous_ready_lines = ""
        else:
            with open(previous_ready_file) as f:
                previous_ready_lines = f.read()
        # print(previous_ready_lines)
        # print("*"*30)
        send_data = dict()
        send_data['name'] = i.get('name')
        send_data['current'] = i.get('current')
        send_data['number'] = i.get('number')
        send_data['ext'] = i.get('ext')
        send_data['mode'] = i.get('mode')
        send_data['code'] = lines
        send_data['ready'] = ready_lines
        send_data['previous_ready'] = previous_ready_lines
        send_data['file_name'] = i.get('file_name')
        send_data['file_source'] = i.get('file_source')
        send_data['file_tab_size'] = i.get('file_tab_size')
        send_data['file_lines'] = i.get('file_lines')
        send_data['score'] = i.get('score')
        send_data['difficulty'] = i.get('difficulty')
        # import pprint
        # pprint.pprint(send_data)
        template_sketch = TemplateSketch(**send_data, template_file_sketches=file_sketch)
        db.session.add(template_sketch)
        db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def test_template(num):
    test = "path"
    data = [
        {
            "name": "Test 1",
            "number": 1,
            "ext": "py",
            "mode": "python",
            "file_name": "step_1",
            "file_source": "web",
            "file_tab_size": 4,
            "file_lines": 1,
            "code": test + "step_1.py",
            "current": True,
            "score": 10,
            "difficulty": "easy",
            "ready": test + "step_1.py",
            "previous_ready": "",
        },
        {
            "name": "Test 2",
            "number": 2,
            "ext": "py",
            "mode": "python",
            "file_name": "step_2",
            "file_source": "web",
            "file_tab_size": 4,
            "file_lines": 1,
            "code": test + "step_2.py",
            "current": False,
            "score": 8,
            "difficulty": "easy",
            "ready": test + "ready_step_2.py",
            "previous_ready": test + "step_1.py",
        },
    ]
    project_sketch = TemplateProjectSketch(name = 'Test')
    db.session.add(project_sketch)
    file_sketch = TemplateFileSketch(name = 'demo.py', template_project_sketches = project_sketch)
    db.session.add(file_sketch)
    lines = ''
    for i in data:
        file = i.get('code')
        with open(file) as f:
            lines = f.read()
        ready_file = i.get('ready')
        with open(ready_file) as f:
            ready_lines = f.read()
        previous_ready_file = i.get('previous_ready')
        if previous_ready_file == "":
            previous_ready_lines = ""
        else:
            with open(previous_ready_file) as f:
                previous_ready_lines = f.read()
        # print(previous_ready_lines)
        # print("*"*30)
        send_data = dict()
        send_data['name'] = i.get('name')
        send_data['current'] = i.get('current')
        send_data['number'] = i.get('number')
        send_data['ext'] = i.get('ext')
        send_data['mode'] = i.get('mode')
        send_data['code'] = lines
        send_data['ready'] = ready_lines
        send_data['previous_ready'] = previous_ready_lines
        send_data['file_name'] = i.get('file_name')
        send_data['file_source'] = i.get('file_source')
        send_data['file_tab_size'] = i.get('file_tab_size')
        send_data['file_lines'] = i.get('file_lines')
        send_data['score'] = i.get('score')
        send_data['difficulty'] = i.get('difficulty')
        # import pprint
        # pprint.pprint(send_data)
        template_sketch = TemplateSketch(**send_data, template_file_sketches=file_sketch)
        db.session.add(template_sketch)
        db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def tetris_template(num):
    tetris = "/home/maratmustafin/2022/microblog-api/games/tetris/"
    data = [
        {
            "name": "Tetris 1",
            "number": 1,
            "ext": "py",
            "mode": "python",
            "file_name": "step_1",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 25,
            "code": tetris + "step_01.py",
            "current": True,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "step_01.py",
            "previous_ready": "",
        },
        {
            "name": "Tetris 2",
            "number": 2,
            "ext": "py",
            "mode": "python",
            "file_name": "step_2",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 2,
            "code": tetris + "step_02.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_02.py",
            "previous_ready": tetris + "step_01.py",
        },
        {
            "name": "Tetris 3",
            "number": 3,
            "ext": "py",
            "mode": "python",
            "file_name": "step_3",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 10,
            "code": tetris + "step_03.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_03.py",
            "previous_ready": tetris + "ready_step_02.py",
        },
        {
            "name": "Tetris 4",
            "number": 4,
            "ext": "py",
            "mode": "python",
            "file_name": "step_4",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 5,
            "code": tetris + "step_04.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_04.py",
            "previous_ready": tetris + "ready_step_03.py",
        },
        {
            "name": "Tetris 5",
            "number": 5,
            "ext": "py",
            "mode": "python",
            "file_name": "step_5",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 5,
            "code": tetris + "step_05.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_05.py",
            "previous_ready": tetris + "ready_step_04.py",
        },
        {
            "name": "Tetris 6",
            "number": 6,
            "ext": "py",
            "mode": "python",
            "file_name": "step_6",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 11,
            "code": tetris + "step_06.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_06.py",
            "previous_ready": tetris + "ready_step_05.py",
        },
        {
            "name": "Tetris 7",
            "number": 7,
            "ext": "py",
            "mode": "python",
            "file_name": "step_7",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 17,
            "code": tetris + "step_07.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_07.py",
            "previous_ready": tetris + "ready_step_06.py",
        },
        {
            "name": "Tetris 8",
            "number": 8,
            "ext": "py",
            "mode": "python",
            "file_name": "step_8",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 9,
            "code": tetris + "step_08.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_08.py",
            "previous_ready": tetris + "ready_step_07.py",
        },
        {
            "name": "Tetris 9",
            "number": 9,
            "ext": "py",
            "mode": "python",
            "file_name": "step_9",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 5,
            "code": tetris + "step_09.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_09.py",
            "previous_ready": tetris + "ready_step_08.py",
        },
        {
            "name": "Tetris 10",
            "number": 10,
            "ext": "py",
            "mode": "python",
            "file_name": "step_10",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 5,
            "code": tetris + "step_10.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_10.py",
            "previous_ready": tetris + "ready_step_09.py",
        },
        {
            "name": "Tetris 11",
            "number": 11,
            "ext": "py",
            "mode": "python",
            "file_name": "step_11",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 4,
            "code": tetris + "step_11.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_11.py",
            "previous_ready": tetris + "ready_step_10.py",
        },
        {
            "name": "Tetris 12",
            "number": 12,
            "ext": "py",
            "mode": "python",
            "file_name": "step_12",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 5,
            "code": tetris + "step_12.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_12.py",
            "previous_ready": tetris + "ready_step_11.py",
        },
        {
            "name": "Tetris 13",
            "number": 13,
            "ext": "py",
            "mode": "python",
            "file_name": "step_13",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 17,
            "code": tetris + "step_13.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_13.py",
            "previous_ready": tetris + "ready_step_12.py",
        },
        {
            "name": "Tetris 14",
            "number": 14,
            "ext": "py",
            "mode": "python",
            "file_name": "step_14",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 14,
            "code": tetris + "step_14.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_14.py",
            "previous_ready": tetris + "ready_step_13.py",
        },
        {
            "name": "Tetris 15",
            "number": 15,
            "ext": "py",
            "mode": "python",
            "file_name": "step_15",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 7,
            "code": tetris + "step_15.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_15.py",
            "previous_ready": tetris + "ready_step_14.py",
        },
        {
            "name": "Tetris 16",
            "number": 16,
            "ext": "py",
            "mode": "python",
            "file_name": "step_16",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 11,
            "code": tetris + "step_16.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_16.py",
            "previous_ready": tetris + "ready_step_15.py",
        },
        {
            "name": "Tetris 17",
            "number": 17,
            "ext": "py",
            "mode": "python",
            "file_name": "step_17",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 33,
            "code": tetris + "step_17.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_17.py",
            "previous_ready": tetris + "ready_step_16.py",
        },
        {
            "name": "Tetris 18",
            "number": 18,
            "ext": "py",
            "mode": "python",
            "file_name": "step_18",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 8,
            "code": tetris + "step_18.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_18.py",
            "previous_ready": tetris + "ready_step_17.py",
        },
        {
            "name": "Tetris 19",
            "number": 19,
            "ext": "py",
            "mode": "python",
            "file_name": "step_19",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 9,
            "code": tetris + "step_19.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_19.py",
            "previous_ready": tetris + "ready_step_18.py",
        },
        {
            "name": "Tetris 20",
            "number": 20,
            "ext": "py",
            "mode": "python",
            "file_name": "step_20",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 12,
            "code": tetris + "step_20.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_20.py",
            "previous_ready": tetris + "ready_step_19.py",
        },
        {
            "name": "Tetris 21",
            "number": 21,
            "ext": "py",
            "mode": "python",
            "file_name": "step_21",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 18,
            "code": tetris + "step_21.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_21.py",
            "previous_ready": tetris + "ready_step_20.py",
        },
        {
            "name": "Tetris 22",
            "number": 22,
            "ext": "py",
            "mode": "python",
            "file_name": "step_22",
            "file_source": "https://github.com/pyGuru123/Python-Games/tree/master/Tetris",
            "file_tab_size": 4,
            "file_lines": 1,
            "code": tetris + "step_22.py",
            "current": False,
            "score": 10,
            "difficulty": "easy",
            "ready": tetris + "ready_step_22.py",
            "previous_ready": tetris + "ready_step_21.py",
        },
    ]
    project_sketch = TemplateProjectSketch(name = 'Tetris')
    db.session.add(project_sketch)
    file_sketch = TemplateFileSketch(name = 'demo.py', template_project_sketches = project_sketch)
    db.session.add(file_sketch)
    lines = ''
    for i in data:
        file = i.get('code')
        with open(file) as f:
            lines = f.read()
        ready_file = i.get('ready')
        with open(ready_file) as f:
            ready_lines = f.read()
        previous_ready_file = i.get('previous_ready')
        if previous_ready_file == "":
            previous_ready_lines = ""
        else:
            with open(previous_ready_file) as f:
                previous_ready_lines = f.read()
        # print(previous_ready_lines)
        # print("*"*30)
        send_data = dict()
        send_data['name'] = i.get('name')
        send_data['current'] = i.get('current')
        send_data['number'] = i.get('number')
        send_data['ext'] = i.get('ext')
        send_data['mode'] = i.get('mode')
        send_data['code'] = lines
        send_data['ready'] = ready_lines
        send_data['previous_ready'] = previous_ready_lines
        send_data['file_name'] = i.get('file_name')
        send_data['file_source'] = i.get('file_source')
        send_data['file_tab_size'] = i.get('file_tab_size')
        send_data['file_lines'] = i.get('file_lines')
        send_data['score'] = i.get('score')
        send_data['difficulty'] = i.get('difficulty')
        # import pprint
        # pprint.pprint(send_data)
        template_sketch = TemplateSketch(**send_data, template_file_sketches=file_sketch)
        db.session.add(template_sketch)
        db.session.commit()
@fake.cli.command()
@click.argument('num', type=int)
def users(num):  # pragma: no cover
    """Create the given number of fake users."""
    users = []
    for i in range(num):
        user = User(username=faker.user_name(), email=faker.email(),
                    about_me=faker.sentence())
        db.session.add(user)
        users.append(user)

    # create some followers as well
    for user in users:
        num_followers = random.randint(0, 5)
        for i in range(num_followers):
            following = random.choice(users)
            if user != following:
                user.follow(following)

    db.session.commit()
    print(num, 'users added.')


@fake.cli.command()
@click.argument('num', type=int)
def posts(num):  # pragma: no cover
    """Create the given number of fake posts, assigned to random users."""
    users = db.session.scalars(User.select()).all()
    for i in range(num):
        user = random.choice(users)
        post = Post(text=faker.paragraph(), author=user,
                    timestamp=faker.date_time_this_year())
        db.session.add(post)
    db.session.commit()
    print(num, 'posts added.')

@fake.cli.command()
@click.argument('num', type=int)
def test_projects(num):
    project_game_sketch = ProjectGameSketch(name='CastleDefense')
    db.session.add(project_game_sketch)
    file_game_sketch = FileGameSketch(name='demo.py',project_game_sketches=project_game_sketch)
    db.session.add(file_game_sketch)
    db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def add_days(num):
    pass

@fake.cli.command()
@click.argument('num', type=int)
def add_level(num):
    levels = [
        {
            "name": "1",
            "xp": 1000
        },
        {
            "name": "2",
            "xp": 2000
        },
        {
            "name": "3",
            "xp": 3000
        },
        {
            "name": "4",
            "xp": 4000
        },
        {
            "name": "5",
            "xp": 5000
        },
        {
            "name": "6",
            "xp": 6000
        },
        {
            "name": "7",
            "xp": 7000
        },
        {
            "name": "8",
            "xp": 8000
        },
        {
            "name": "9",
            "xp": 9000
        },
        {
            "name": "10",
            "xp": 10000
        },
    ]
    for level in levels:
        level = Level(**level)
        db.session.add(level)
    db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def add_to_user(num):
    user = db.session.get(User, num)
    # template_project_sketches = db.session.scalars('select * from template_project_sketches').all()
    temp_project = db.session.get(TemplateProjectSketch, 6)
    # for t_project in template_project_sketches:
    # template_project_sketch = db.session.get(TemplateProjectSketch, t_project)
    # pdb.set_trace()
    project_game_sketch = ProjectGameSketch(user=user, name=temp_project.__dict__.get('name'))
    db.session.add(project_game_sketch)
    # db.session.commit()
    for t_file in temp_project.template_file_sketches:
        file_game_sketch = FileGameSketch(user=user,name=t_file.name,code='',project_game_sketches=project_game_sketch)
        db.session.add(file_game_sketch)
        # db.session.commit()
        for t_sketch in t_file.template_sketches:
            t_sketch.__dict__.pop("_sa_instance_state")
            t_sketch.__dict__.pop("id")
            t_sketch.__dict__.pop("template_file_sketch_id")
            game_sketch = GameSketch(user=user,file_game_sketches=file_game_sketch, **t_sketch.__dict__)
            db.session.add(game_sketch)
    db.session.add(user)
    db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def init_game(num):
    user = db.session.get(User, 1)
    user.project_game_sketches[2].is_done = False
    user.file_game_sketches[0].is_done = False
    db.session.add(user)
    for i in user.game_sketches:
        if i.id == 65:
            i.is_done = 'init'
            i.current = True
            db.session.add(i)
        if i.id == 66:
            i.is_done = 'init'
            i.current = False
            db.session.add(i)
    db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def add_new_users(num):
    con = sqlite3.connect('path')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM users');
    massive = []
    for r in res:
        users = {}
        users['id'] = r[0]
        users['username'] = r[1]
        users['email'] = None
        users['nickname'] = r[3]
        users['role'] = 'student'
        users['password_hash'] = r[4]
        users['about_me'] = None
        users['first_seen'] = parser.parse(r[6])
        users['last_seen'] = parser.parse(r[7])
        massive.append(users)
    print(massive)
    for mass in massive:
        user = User(**mass)
        db.session.add(user)
    db.session.commit()
    users = db.session.scalars(User.select()).all()
    print(users)


@fake.cli.command()
@click.argument('num', type=int)
def add_new_project(num):
    con = sqlite3.connect('path')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM project_game_sketches');
    massive = []
    for r in res.fetchall():
        projects = {}
        projects['id'] = r[0]
        projects['name'] = r[1]
        projects['description'] = None
        projects['timestamp'] = parser.parse(r[3])
        projects['user_id'] = r[4]
        massive.append(projects)

    for mass in massive:
        project = ProjectGameSketch(**mass)
        db.session.add(project)
    db.session.commit()
    projects = db.session.scalars(ProjectGameSketch.select()).all()
    print(projects)

@fake.cli.command()
@click.argument('num', type=int)
def add_new_file(num):
    con = sqlite3.connect('/home/maratmustafin/2022/microblog-api/db1.sqlite')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM file_game_sketches');
    massive = []
    for r in res.fetchall():
        files = {}
        files['id'] = r[0]
        files['name'] = r[1]
        files['code'] = r[2]
        files['previous_code'] = r[3]
        files['timestamp'] = parser.parse(r[4])
        files['project_game_sketch_id'] = r[5]
        files['user_id'] = r[6]
        massive.append(files)
    for mass in massive:
        file = FileGameSketch(**mass)
        db.session.add(file)
    db.session.commit()
    users = db.session.scalars(FileGameSketch.select()).all()
    print(users)

@fake.cli.command()
@click.argument('num', type=int)
def add_new_sketch(num):
    con = sqlite3.connect('path')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM game_sketches');
    massive = []
    for r in res.fetchall():
        sketches = {}
        sketches['id'] = r[0]
        sketches['name'] = r[1]
        sketches['number'] = r[2]
        sketches['current'] = r[3]
        sketches['code'] = r[4]
        sketches['ext'] = r[5]
        sketches['mode'] = r[6]
        sketches['file_name'] = r[7]
        sketches['file_source'] = r[8]
        sketches['file_tab_size'] = r[9]
        sketches['file_lines'] = r[10]
        sketches['timestamp']= parser.parse(r[11])
        sketches['user_code']= r[12]
        sketches['current_line'] = r[13]
        sketches['current_char'] = r[14]
        sketches['ready'] = r[15]
        sketches['previous_ready'] = r[16]
        sketches['score'] = r[17]
        sketches['difficulty'] = r[18]
        sketches['is_done'] = r[19]
        sketches['file_game_sketch_id'] = r[20]
        sketches['user_id'] = r[21]
        massive.append(sketches)

    for mass in massive:
        sketch = GameSketch(**mass)
        db.session.add(sketch)
    db.session.commit()
    sketches = db.session.scalars(GameSketch.select()).all()
    print(sketches)

@fake.cli.command()
@click.argument('num', type=int)
def update_game_sketch_line(num):
    user = db.session.get(User, num)
    tetris = user.file_game_sketches[1].game_sketches[10]
    print(tetris.file_lines)
    tetris.file_lines = 4
    db.session.add(tetris)
    db.session.commit()
    print(tetris.file_lines)

@fake.cli.command()
@click.argument('num', type=int)
def test_runner(num):
    tetris = "path"
    path = tetris + "ready_step_10.py"
    # with open(path) as f:
    #     lines = f.readlines()
    #     print(len(lines))
    file = Files(path=path)
    db.session.add(file)
    db.session.commit()
    # file = db.session.get(Files, 1)
    # line = Lines(start=4,end=14,step=1,files = file)
    # db.session.add(line)
    # db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def fighter_template(num):
    fight_game = 'path'
    data = [
        {
            "name": "Fighter 1",
            "number": 1,
            "ext": "py",
            "mode": "python",
            "file_name": "step01",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 12,
            "code": fight_game + "step01.py",
            "current": True,
            "score": 6,
            "difficulty": "easy",
            "ready": fight_game + "step01.py",
            "previous_ready": "",
        },
        {
            "name": "Fighter 2",
            "number": 2,
            "ext": "py",
            "mode": "python",
            "file_name": "step02",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 11,
            "code": fight_game + "step02.py",
            "current": False,
            "score": 5,
            "difficulty": "easy",
            "ready": fight_game + "ready_step02.py",
            "previous_ready": fight_game + "step01.py",
        },
        {
            "name": "Fighter 3",
            "number": 3,
            "ext": "py",
            "mode": "python",
            "file_name": "step01",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 4,
            "code": fight_game + "step03.py",
            "current": False,
            "score": 2,
            "difficulty": "easy",
            "ready": fight_game + "ready_step03.py",
            "previous_ready": fight_game + "ready_step02.py",
        },
        {
            "name": "Fighter 4",
            "number": 4,
            "ext": "py",
            "mode": "python",
            "file_name": "step04",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 21,
            "code": fight_game + "step04.py",
            "current": False,
            "score": 11,
            "difficulty": "easy",
            "ready": fight_game + "ready_step04.py",
            "previous_ready": fight_game + "ready_step03.py",
        },
        {
            "name": "Fighter 5",
            "number": 5,
            "ext": "py",
            "mode": "python",
            "file_name": "step05",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 0,
            "code": fight_game + "step05.py",
            "is_self": True,
            "current": False,
            "score": 1,
            "difficulty": "easy",
            "ready": fight_game + "ready_step04.py",
            "previous_ready": fight_game + "ready_step04.py",
        },
        {
            "name": "Fighter 6",
            "number": 6,
            "ext": "py",
            "mode": "python",
            "file_name": "step06",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 3,
            "code": fight_game + "step06.py",
            "current": False,
            "score": 2,
            "difficulty": "easy",
            "ready": fight_game + "ready_step06.py",
            "previous_ready": fight_game + "ready_step04.py",
        },
        {
            "name": "Fighter 7",
            "number": 7,
            "ext": "py",
            "mode": "python",
            "file_name": "step07",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 7,
            "code": fight_game + "step07.py",
            "current": False,
            "score": 4,
            "difficulty": "easy",
            "ready": fight_game + "ready_step07.py",
            "previous_ready": fight_game + "ready_step06.py",
        },
        {
            "name": "Fighter 8",
            "number": 8,
            "ext": "py",
            "mode": "python",
            "file_name": "step08",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 6,
            "code": fight_game + "step08.py",
            "current": False,
            "score":  6,
            "difficulty": "easy",
            "ready": fight_game + "ready_step08.py",
            "previous_ready": fight_game + "ready_step07.py",
        },
        {
            "name": "Fighter 9",
            "number": 9,
            "ext": "py",
            "mode": "python",
            "file_name": "step09",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 6,
            "code": fight_game + "step09.py",
            "current": False,
            "score": 3,
            "difficulty": "easy",
            "ready": fight_game + "ready_step09.py",
            "previous_ready": fight_game + "ready_step08.py",
        },
        {
            "name": "Fighter 10",
            "number": 10,
            "ext": "py",
            "mode": "python",
            "file_name": "step10",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 1,
            "code": fight_game + "step10.py",
            "current": False,
            "score": 1,
            "difficulty": "easy",
            "ready": fight_game + "ready_step10.py",
            "previous_ready": fight_game + "ready_step09.py",
        },
        {
            "name": "Fighter 11",
            "number": 11,
            "ext": "py",
            "mode": "python",
            "file_name": "step11",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 12,
            "code": fight_game + "step11.py",
            "current": False,
            "score": 7,
            "difficulty": "easy",
            "ready": fight_game + "ready_step11.py",
            "previous_ready": fight_game + "ready_step10.py",
        },
        {
            "name": "Fighter 12",
            "number": 12,
            "ext": "py",
            "mode": "python",
            "file_name": "step12",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 5,
            "code": fight_game + "step12.py",
            "current": False,
            "score": 3,
            "difficulty": "easy",
            "ready": fight_game + "ready_step12.py",
            "previous_ready": fight_game + "ready_step11.py",
        },
        {
            "name": "Fighter 13",
            "number": 13,
            "ext": "py",
            "mode": "python",
            "file_name": "step13",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 5,
            "code": fight_game + "step13.py",
            "current": False,
            "score": 3,
            "difficulty": "easy",
            "ready": fight_game + "ready_step13.py",
            "previous_ready": fight_game + "ready_step12.py",
        },
        {
            "name": "Fighter 14",
            "number": 14,
            "ext": "py",
            "mode": "python",
            "file_name": "step14",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 3,
            "code": fight_game + "step14.py",
            "current": False,
            "score": 2,
            "difficulty": "easy",
            "ready": fight_game + "ready_step14.py",
            "previous_ready": fight_game + "ready_step13.py",
        },
        {
            "name": "Fighter 15",
            "number": 15,
            "ext": "py",
            "mode": "python",
            "file_name": "step15",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 8,
            "code": fight_game + "step15.py",
            "current": False,
            "score": 6,
            "difficulty": "easy",
            "ready": fight_game + "ready_step15.py",
            "previous_ready": fight_game + "ready_step14.py",
        }
    ]
    project_sketch = TemplateProjectSketch(name = 'Fight Game')
    db.session.add(project_sketch)
    file_sketch = TemplateFileSketch(name = 'main.py', template_project_sketches = project_sketch)
    db.session.add(file_sketch)
    lines = ''
    for i in data:
        file = i.get('code')
        if file != "":
            with open(file) as f:
                lines = f.read()
        else:
            lines = ""
        ready_file = i.get('ready')
        with open(ready_file) as f:
            ready_lines = f.read()
        previous_ready_file = i.get('previous_ready')
        if previous_ready_file == "":
            previous_ready_lines = ""
        else:
            with open(previous_ready_file) as f:
                previous_ready_lines = f.read()
        # print(previous_ready_lines)
        # print("*"*30)
        send_data = dict()
        send_data['name'] = i.get('name')
        send_data['current'] = i.get('current')
        send_data['number'] = i.get('number')
        send_data['ext'] = i.get('ext')
        send_data['mode'] = i.get('mode')
        send_data['code'] = lines
        send_data['ready'] = ready_lines
        send_data['previous_ready'] = previous_ready_lines
        send_data['file_name'] = i.get('file_name')
        send_data['file_source'] = i.get('file_source')
        send_data['file_tab_size'] = i.get('file_tab_size')
        send_data['file_lines'] = i.get('file_lines')
        send_data['score'] = i.get('score')
        send_data['difficulty'] = i.get('difficulty')
        # import pprint
        # pprint.pprint(send_data)
        template_sketch = TemplateSketch(**send_data, template_file_sketches=file_sketch)
        db.session.add(template_sketch)
        db.session.commit()



@fake.cli.command()
@click.argument('num', type=int)
def upd_courses(num):
    path = 'path'
    files = ['course_11.py','course_12.py','course_13.py','course_14.py','course_15.py']
    for f in files:
        file = path + '/'+ f
        save = Files(path=file)
        db.session.add(save)
        db.session.commit()

@fake.cli.command()
@click.argument('num', type=int)
def tester1(num):
    file4 = db.session.get(Files,9)
    file5 = db.session.get(Files,10)
    code = file5.difference(file4)
    check = ''.join(code)
    # print(check)
    import os, sys, argparse
    from io import StringIO

    def reindent(buffer, tabs=4, tospaces=False, nospaces=False, fromtabs=None, backupsuffix="~"):
        if fromtabs == None:
            fromtabs = tabs
        temporary = []
        outlines = []
        with StringIO(buffer) as fin:
            buf = fin.read()
            lines = buf.splitlines()
            for lineno, line in enumerate(lines):
                line = line.rstrip()
                indent = 0
                pos = 0
                if len(line) != 0:
                    while pos < len(line) and line[pos] in [' ', '    ']:
                        if line[pos] == ' ':
                            indent = indent + 1
                        else:
                            break
                        pos = pos + 1
                    line = line[pos:]
                    if indent - (indent//tabs)*tabs > 0:
                        if indent == 9:
                            try:
                                # if lines[lineno-1].split()[0] not in ['if', 'for', 'with', 'class', 'def', 'else:', 'elif']:
                                #     line = line
                                if lines[lineno-1].split()[0] == 'if' \
                                    or lines[lineno-1].split()[0] == 'for' \
                                    or lines[lineno-1].split()[0] == 'with' \
                                    or lines[lineno-1].split()[0] == 'class' \
                                    or lines[lineno-1].split()[0] == 'def' \
                                    or lines[lineno-1].split()[0] == 'else:' \
                                    or lines[lineno-1].split()[0] == 'elif':
                                    line = (' '*(indent - (indent//tabs)*tabs)) * 4 + line
                                elif line[:2] == 'if' \
                                    or line[:3] == 'for' \
                                        or line[:4] == 'with' \
                                            or line[:5] == 'class' \
                                                or line[:3] == 'def' \
                                                    or line[:4] == 'else' \
                                                        or line[:4] == 'elif':
                                    line = (' '*(indent - (indent//tabs)*tabs)) * 4 + line
                                elif lines[lineno-1][:9] == '         ':
                                    line = (' '*(indent - (indent//tabs)*tabs)) * 4 + line
                                else:
                                    line = line
                            except:
                                line = line
                        if indent == 13:
                            # if  lines[lineno-1].split()[0] == 'if' \
                            #     or lines[lineno-1].split()[0] == 'for' \
                            #     or lines[lineno-1].split()[0] == 'with' \
                            #     or lines[lineno-1].split()[0] == 'class' \
                            #     or lines[lineno-1].split()[0] == 'def' \
                            #     or lines[lineno-1].split()[0] == 'else:' \
                            #     or lines[lineno-1].split()[0] == 'elif' \
                            #     and lines[lineno-1].split()[0] not in [' ','  ','   ','    ']:
                            #     line = (' '*(indent - (indent//tabs)*tabs)) * 4 + line                               
                            if lines[lineno-1].split()[0] == 'if' \
                                or lines[lineno-1].split()[0] == 'for' \
                                or lines[lineno-1].split()[0] == 'with' \
                                or lines[lineno-1].split()[0] == 'class' \
                                or lines[lineno-1].split()[0] == 'def' \
                                or lines[lineno-1].split()[0] == 'else:' \
                                or lines[lineno-1].split()[0] == 'elif':
                                line = (' '*(indent - (indent//tabs)*tabs)) * 8 + line
                            elif line[:2] == 'if' \
                                 or line[:3] == 'for' \
                                     or line[:4] == 'with' \
                                        or line[:5] == 'class' \
                                             or line[:3] == 'def' \
                                                or line[:4] == 'else' \
                                                    or line[:4] == 'elif':
                                line = (' '*(indent - (indent//tabs)*tabs)) * 8 + line
                            elif lines[lineno-1][:17] == '                 ' \
                                or lines[lineno-1][:13] == '             ':
                                line = (' '*(indent - (indent//tabs)*tabs)) * 8 + line
                            else:
                                line = line
                        if indent == 17:
                            if lines[lineno-1].split()[0] == 'if' \
                                or lines[lineno-1].split()[0] == 'for' \
                                or lines[lineno-1].split()[0] == 'with' \
                                or lines[lineno-1].split()[0] == 'class' \
                                or lines[lineno-1].split()[0] == 'def' \
                                or lines[lineno-1].split()[0] == 'else:' \
                                or lines[lineno-1].split()[0] == 'elif':
                                line = (' '*(indent - (indent//tabs)*tabs)) * 12 + line
                            elif line[:2] == 'if' \
                                 or line[:3] == 'for' \
                                     or line[:4] == 'with' \
                                        or line[:5] == 'class' \
                                             or line[:3] == 'def' \
                                                or line[:4] == 'else' \
                                                    or line[:4] == 'elif':
                                line = (' '*(indent - (indent//tabs)*tabs)) * 12 + line
                            else:
                                line = line
                    print(indent, line)
                    outlines.append(line)
        return "\n".join(outlines)
    wtf = reindent(check)
    # print(wtf)


@fake.cli.command()
@click.argument('num', type=int)
def fighter_template_second(num):
    fight_game = 'path'

    data = [
        {
            "name": "Fighter 16",
            "number": 16,
            "ext": "py",
            "mode": "python",
            "file_name": "step16",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 9,
            "code": fight_game + "step16.py",
            "current": False,
            "score": 6,
            "difficulty": "easy",
            "ready": fight_game + "ready_step16.py",
            "previous_ready": fight_game + "ready_step15.py",
        },
        {
            "name": "Fighter 17",
            "number": 17,
            "ext": "py",
            "mode": "python",
            "file_name": "step17",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 9,
            "code": fight_game + "step17.py",
            "current": False,
            "score": 6,
            "difficulty": "easy",
            "ready": fight_game + "ready_step17.py",
            "previous_ready": fight_game + "ready_step16.py",
        },
        {
            "name": "Fighter 18",
            "number": 18,
            "ext": "py",
            "mode": "python",
            "file_name": "step18",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 11,
            "code": fight_game + "step18.py",
            "current": False,
            "score": 6,
            "difficulty": "easy",
            "ready": fight_game + "ready_step18.py",
            "previous_ready": fight_game + "ready_step17.py",
        },
        {
            "name": "Fighter 19",
            "number": 19,
            "ext": "py",
            "mode": "python",
            "file_name": "step16",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 1,
            "code": fight_game + "step19.py",
            "current": False,
            "score": 1,
            "difficulty": "easy",
            "ready": fight_game + "ready_step19.py",
            "previous_ready": fight_game + "ready_step18.py",
        },
        {
            "name": "Fighter 20",
            "number": 20,
            "ext": "py",
            "mode": "python",
            "file_name": "step20",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 14,
            "code": fight_game + "step20.py",
            "current": False,
            "score": 7,
            "difficulty": "easy",
            "ready": fight_game + "ready_step20.py",
            "previous_ready": fight_game + "ready_step19.py",
        },
        {
            "name": "Fighter 21",
            "number": 21,
            "ext": "py",
            "mode": "python",
            "file_name": "step21",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 4,
            "code": fight_game + "step21.py",
            "current": False,
            "score": 3,
            "difficulty": "easy",
            "ready": fight_game + "ready_step21.py",
            "previous_ready": fight_game + "ready_step20.py",
        },
        {
            "name": "Fighter 22",
            "number": 16,
            "ext": "py",
            "mode": "python",
            "file_name": "step22",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 13,
            "code": fight_game + "step22.py",
            "current": False,
            "score": 5,
            "difficulty": "easy",
            "ready": fight_game + "ready_step22.py",
            "previous_ready": fight_game + "ready_step21.py",
        },
        {
            "name": "Fighter 23",
            "number": 23,
            "ext": "py",
            "mode": "python",
            "file_name": "step23",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 15,
            "code": fight_game + "step23.py",
            "current": False,
            "score": 8,
            "difficulty": "easy",
            "ready": fight_game + "ready_step23.py",
            "previous_ready": fight_game + "ready_step22.py",
        },
        {
            "name": "Fighter 24",
            "number": 24,
            "ext": "py",
            "mode": "python",
            "file_name": "step24",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 2,
            "code": fight_game + "step24.py",
            "current": False,
            "score": 1,
            "difficulty": "easy",
            "ready": fight_game + "ready_step24.py",
            "previous_ready": fight_game + "ready_step23.py",
        },
        {
            "name": "Fighter 25",
            "number": 25,
            "ext": "py",
            "mode": "python",
            "file_name": "step25",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 5,
            "code": fight_game + "step25.py",
            "current": False,
            "score": 2,
            "difficulty": "easy",
            "ready": fight_game + "ready_step25.py",
            "previous_ready": fight_game + "ready_step24.py",
        },
        {
            "name": "Fighter 26",
            "number": 26,
            "ext": "py",
            "mode": "python",
            "file_name": "step26",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 11,
            "code": fight_game + "step26.py",
            "current": False,
            "score": 6,
            "difficulty": "easy",
            "ready": fight_game + "ready_step26.py",
            "previous_ready": fight_game + "ready_step25.py",
        },
        {
            "name": "Fighter 27",
            "number": 27,
            "ext": "py",
            "mode": "python",
            "file_name": "step27",
            "file_source": "https://www.youtube.com/watch?v=s5bd9KMSSW4",
            "file_tab_size": 4,
            "file_lines": 3,
            "code": fight_game + "step27.py",
            "current": False,
            "score": 1,
            "difficulty": "easy",
            "ready": fight_game + "ready_step27.py",
            "previous_ready": fight_game + "ready_step26.py",
        },
    ]

    project_sketch = db.session.get(TemplateFileSketch, 1)
    # db.session.add(project_sketch)
    # file_sketch = TemplateFileSketch(name = 'main.py', template_project_sketches = project_sketch)
    # db.session.add(file_sketch)
    file_sketch = db.session.get(TemplateFileSketch, 1)
    lines = ''
    for i in data:
        file = i.get('code')
        if file != "":
            with open(file) as f:
                lines = f.read()
        else:
            lines = ""
        ready_file = i.get('ready')
        with open(ready_file) as f:
            ready_lines = f.read()
        previous_ready_file = i.get('previous_ready')
        if previous_ready_file == "":
            previous_ready_lines = ""
        else:
            with open(previous_ready_file) as f:
                previous_ready_lines = f.read()
        # print(previous_ready_lines)
        # print("*"*30)
        send_data = dict()
        send_data['name'] = i.get('name')
        send_data['current'] = i.get('current')
        send_data['number'] = i.get('number')
        send_data['ext'] = i.get('ext')
        send_data['mode'] = i.get('mode')
        send_data['code'] = lines
        send_data['ready'] = ready_lines
        send_data['previous_ready'] = previous_ready_lines
        send_data['file_name'] = i.get('file_name')
        send_data['file_source'] = i.get('file_source')
        send_data['file_tab_size'] = i.get('file_tab_size')
        send_data['file_lines'] = i.get('file_lines')
        send_data['score'] = i.get('score')
        send_data['difficulty'] = i.get('difficulty')
        # import pprint
        # pprint.pprint(send_data)
        template_sketch = TemplateSketch(**send_data, template_file_sketches=file_sketch)
        db.session.add(template_sketch)
        db.session.commit()