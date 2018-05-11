import sqlite3
from tasker import checker

SQL_SELECT_ALL = "SELECT id, header, description, start_date, end_date, status FROM tasker"

SQL_INSERT_TASK = "INSERT INTO tasker (header, description, start_date, end_date) VALUES (?, ?, ?, ?)"

SQL_CLOSE_TASK =  "UPDATE tasker SET status=?, end_date=? WHERE id=?"

SQL_OPEN_TASK = "UPDATE tasker SET status=?, start_date=?, end_date=? WHERE id=?"

SQL_UPDATE_TASK = "UPDATE tasker SET header=?, description=?, start_date=?, end_date=? WHERE id=?"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


def connect(db_name=None):
    if db_name is None:
        db_name = ':memory:'

    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory

    return conn


def initialize(conn, creation_schema):
    """Инициализирует БД"""
    with conn, open(creation_schema) as f:
        conn.executescript(f.read())


def show_tasks(conn):
    """Выводит список всех задач"""
    with conn:
        checker.status_changer(conn)
        cursor = conn.execute(SQL_SELECT_ALL)
        return cursor.fetchall()

def add_task(conn, header, description, start_date, end_date):
    """Добавляет новую задачу"""
    checker.date_validate(start_date)
    checker.date_validate(end_date)
    checker.date_compare(start_date, end_date)

    with conn:
        cursor = conn.execute(SQL_INSERT_TASK, (header, description, start_date, end_date))


def edit_task(conn, task_id, header, description, start_date, end_date):
    """Редактирует задачу"""
    checker.date_validate(start_date)
    checker.date_validate(end_date)
    checker.date_compare(start_date, end_date)

    with conn:
        cursor = conn.execute(SQL_UPDATE_TASK, (header, description, start_date, end_date, task_id))


def close_task(conn, task_id, end_date):
    """Завершает задачу"""
    checker.date_validate(end_date)

    with conn:
        cursor = conn.execute(SQL_CLOSE_TASK, ('closed', end_date, task_id))


def reopen_task(conn, task_id, start_date, end_date):
    """Переоткрывает задачу"""
    checker.date_validate(start_date)
    checker.date_validate(end_date)
    checker.date_compare(start_date, end_date)

    with conn:
        cursor = conn.execute(SQL_OPEN_TASK, ('opened', start_date, end_date, task_id))
