'''
A RemindmeRepository is a Repository for storing and retrieving Remindmes.
'''

import sqlite3
from .Remindme import Remindme


class RemindmeRepository:
    '''Repository of Remindmes.'''

    def __init__(self, db_file):
        '''Create a sqlite3 database for remindmes.'''
        self.__db = None
        self.__cursor = None
        self.__remindmes = []
        with sqlite3.connect(db_file) as db:
            self.__db = db
            self.__cursor = db.cursor()
            try:
                sql = 'CREATE TABLE IF NOT EXISTS remindmes(title, content)'
                self.__cursor.execute(sql)
                # sql = 'CREATE UNIQUE INDEX indices ON remindmes(title)'
                # self.__cursor.execute(sql)
                self.__db.commit()
                self.restore_remindmes()
            except Exception:
                raise Exception()

    def __register_remindme(self, remindme):
        self.__remindmes.append(remindme)

    def restore_remindmes(self):
        '''Restores previously stored remindmes from the database.'''
        try:
            sql = 'SELECT title, content FROM remindmes'
            for item in self.__cursor.execute(sql).fetchall():
                remindme = Remindme(item[0], item[1], self)
                self.__register_remindme(remindme)
        except sqlite3.OperationalError:
            pass
        return self

    def insert_remindme(self, remindme):
        '''Insert remindme into this repository.'''
        try:
            sql = 'INSERT INTO remindmes VALUES (?,?)'
            self.__cursor.execute(sql, (remindme.get_title(), remindme.get_content(),))
            self.__db.commit()
            self.__register_remindme(remindme)
            return True
        except sqlite3.OperationalError:
            self.__db.rollback()
            return False

    def create_remindme(self, title, content):
        '''Creates a new remindme in this repository.'''
        remindme = Remindme(title, content, self)
        try:
            self.insert_remindme(remindme)
            return remindme
        except:
            return None

    def remove_remindme(self, remindme):
        '''Remove remindme from this repository.'''
        try:
            sql = 'DELETE FROM remindmes WHERE keyword == "{0}" '
            sql = sql.format(remindme.get_title())
            self.__cursor.execute(sql)
            self.__db.commit()
            return True
        except:
            self.__db.rollback()
            return False

    def remove_remindmes(self):
        '''Removes all remindmes from this repository.'''
        for remindme in self.__remindmes:
            self.remove_remindme(remindme)

    def __filter_out_deleted(self):
        '''Filters out deleted remindmes.'''
        self.__remindmes = [r for r in self.__remindmes
            if r.get_props()["deleted"] is False]

    def get_remindmes(self):
        '''Return remindmes from database.'''
        self.__filter_out_deleted()
        return self.__remindmes

    def save_remindmes(self):
        '''Save all remindmes.'''
        self.__filter_out_deleted()
        for remindme in self.__remindmes:
            remindme.save()

    def find(self, qualify):
        '''Search through the remindmes.'''
        self.__filter_out_deleted()
        return [x for x in self.__remindmes if qualify(x)]

    def find_by_title(self, title):
        '''Find the remindme by title.'''
        return self.find(lambda remindme: remindme.get_title() == title)[0] or None
