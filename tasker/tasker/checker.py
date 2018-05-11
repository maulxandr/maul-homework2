import datetime



def date_validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Неправильный формат даты. Должно быть 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'")


def date_compare(start_date, end_date):
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        if end_date < start_date:
            raise ValueError

    except ValueError:
        raise ValueError('Дата окончания задачи не может быть в прошлом!')


def id_check(conn, task_id):
    with conn:
        cursor = conn.execute("SELECT id FROM tasker WHERE id=?", (task_id,))
        try:
            if cursor.fetchone() is None:
                raise ValueError

        except ValueError:
            raise ValueError('Нет такой задачи!')


def status_changer(conn):
    with conn:
        cursor = conn.execute("SELECT id, end_date, status FROM tasker")
        rows = cursor.fetchall()

        for row in rows:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_date = datetime.datetime.strptime(row['end_date'], '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
            task_id = row['id']
            status = row['status']

            if end_date < now and status == 'opened':
                cursor = conn.execute("UPDATE tasker SET status=? WHERE id=?", ('expired', task_id))
