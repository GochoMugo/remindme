import os
import sqlite3


home = os.path.expanduser('~')
db_file = os.path.join(home, '.remindme.db')


def createTable(db, table="remindmes"):
    try:
        cursor = db.cursor()
        sql = 'CREATE TABLE {0}(keyword, content)'
        sql = sql.format(table)
        cursor.execute(sql)
        sql = 'CREATE UNIQUE INDEX indices ON {0}(keyword)'
        sql = sql.format(table)
        cursor.execute(sql)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False


def read(table='remindmes', db_file=db_file):
    content = []
    with sqlite3.connect(db_file) as db:
        cursor = db.cursor()
        try:
            sql = 'SELECT keyword, content FROM {0}'.format(table)
            for item in cursor.execute(sql).fetchall():
                content.append(item)
        except sqlite3.OperationalError:
            createTable(db)
    return content


def write(keyword, content, table='remindmes', db_file=db_file):
    with sqlite3.connect(db_file) as db:
        try:
            cursor = db.cursor()
            sql = 'INSERT INTO {0} VALUES (?,?)'.format(table)
            cursor.execute(sql, (keyword, content,))
            db.commit()
            return True
        except sqlite3.OperationalError:
            res = createTable(db)
            if res:
                return write(keyword, content, table, db_file)
            else:
                db.rollback()
                return False
    return False


def search(content, keyword):
    for item in content:
        if item[0] == keyword:
            return item[1]
    return False


def add(content, keyword, new_content, db_file=db_file):
    if not search(content, keyword):
        return write(keyword, new_content,"remindmes", db_file)
    return False


def remove(content, keyword, table="remindmes", db_file=db_file):
    if search(content, keyword) is not False:
        try:
            with sqlite3.connect(db_file) as db:
                sql = 'DELETE FROM {0} WHERE keyword == "{1}"'
                sql = sql.format(table, keyword)
                db.execute(sql)
                db.commit()
                return True
        except:
            db.rollback()
            return False
    else:
        return False
