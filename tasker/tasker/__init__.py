import os.path as Path
import sys
import datetime
from tasker import storage, checker
from collections import OrderedDict, namedtuple


get_connection = lambda : storage.connect("tasker.sqlite")


Action = namedtuple('Action', ['func', 'name'])
actions = OrderedDict()


def menu_action(cmd, name):
    def decorator(func):
        actions[cmd] = Action(func=func, name=name)
        return func
    return decorator


@menu_action('1', 'Вывести весь список задач')
def action_show_tasks():
    """Вывести весь список задач"""
    with get_connection() as conn:
        rows = storage.show_tasks(conn)

    print("""
Ежедневник
    
ID - Заголовок - Описание - Время начала - Время окончания - Статус
""")
    template = '{row[id]} - {row[header]} - {row[description]} - {row[start_date]} - {row[end_date]} - {row[status]}'

    for row in rows:
        print(template.format(row=row))



@menu_action('2', 'Добавить задачу')
def action_add(): # Добавить задачу
    header = input("\nВведите название задачи: ")
    description = input("\nВведите описание задачи: ")
    start_date = input("\nВведите время начала задачи в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС' (по умолчанию - текущее время): ")
    end_date = input("\nВведите время окончания задачи в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС': ")

    if start_date == '':
        start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = storage.add_task(conn, header, description, start_date, end_date)

    print("Задача добавлена:\nЗаголовок: {}\nОписание: {}\nВремя начала: {}\nВремя окончания: {}".format(header, description, start_date, end_date))


@menu_action('3', 'Отредактировать задачу')
def action_edit():
    action_show_tasks()
    task_id = input("\nВыберите задачу по ID: ")

    with get_connection() as conn:
        cursor = checker.id_check(conn, task_id)

    header = input("\nВведите название задачи: ")
    description = input("\nВведите описание задачи: ")
    start_date = input("\nВведите время начала задачи в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС' (по умолчанию - текущее время): ")
    end_date = input("\nВведите время окончания задачи в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС': ")

    if start_date == '':
        start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = storage.edit_task(conn, task_id, header, description, start_date, end_date)

    print("Задача обновлена:\nЗаголовок: {}\nОписание: {}\nВремя начала: {}\nВремя окончания: {}".format(header, description, start_date, end_date))


@menu_action('4', 'Завершить задачу')
def action_close():
    action_show_tasks()
    task_id = input("\nВыберите задачу по ID: ")

    with get_connection() as conn:
        cursor = checker.id_check(conn, task_id)

    end_date = input("\nВведите фактическое время окончания задачи в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС' (по умолчанию - текущее время): ")

    if end_date == '':
        end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = storage.close_task(conn, task_id, end_date)


@menu_action('5', 'Начать задачу сначала')
def action_reopen():
    action_show_tasks()
    task_id = input("\nВыберите задачу по ID: ")

    with get_connection() as conn:
        cursor = checker.id_check(conn, task_id)

    start_date = input("\nВведите время начала задачи в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС' (по умолчанию - текущее время): ")
    end_date = input("\nВведите время окончания задачи в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС': ")

    if start_date == '':
        start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = storage.reopen_task(conn, task_id, start_date, end_date)


@menu_action('m', 'Показать меню')
def action_show_menu():
    menu = []

    for cmd, action in actions.items():
        menu.append('{}. {}'.format(cmd, action.name))

    print('\n'.join(menu))


@menu_action('q', 'Выход')
def action_exit():
    sys.exit(0)


def main():
    creation_schema = Path.join(
        Path.dirname(__file__), 'schema.sql'
    )

    with get_connection() as conn:
        storage.initialize(conn, creation_schema)

    action_show_menu()

    while True:
        cmd = input('\nВведите команду: ')
        action = actions.get(cmd)

        if action:
            action.func()
        else:
            print('Неизвестная команда')
