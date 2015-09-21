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
        self.__deleted_remindmes = []
        with sqlite3.connect(db_file) as db:
            self.__db = db
            self.__cursor = db.cursor()
            try:
                sql = 'CREATE TABLE IF NOT EXISTS remindmes(title, content)'
                self.__cursor.execute(sql)
                sql = 'CREATE UNIQUE INDEX IF NOT EXISTS indices ON remindmes(title)'
                self.__cursor.execute(sql)
                self.__db.commit()
                self.__restore_remindmes()
            except Exception:
                raise Exception()

    def __register_remindme(self, remindme):
        self.__remindmes.append(remindme)

    def __restore_remindmes(self):
        '''Restores previously stored remindmes from the database.'''
        try:
            sql = 'SELECT title, content FROM remindmes'
            for item in self.__cursor.execute(sql).fetchall():
                remindme = Remindme(item[0], item[1], repository=self)
                self.__register_remindme(remindme)
        except sqlite3.OperationalError:
            pass
        return self

    def insert_remindme(self, remindme):
        '''Insert remindme into this repository.'''
        try:
            remindme.set_repository(self)
            sql = 'INSERT INTO remindmes VALUES (?,?)'
            self.__cursor.execute(sql, (remindme.get_title(), remindme.get_content(),))
            self.__db.commit()
            self.__register_remindme(remindme)
            return True
        except Exception:
            self.__db.rollback()
            return False

    def create_remindme(self, title, content):
        '''Creates a new remindme in this repository.'''
        remindme = Remindme(title, content, self)
        status = self.insert_remindme(remindme)
        return remindme if status is True else False

    def update_remindme(self, remindme):
        '''Updates a remindme in this repository.'''
        try:
            sql = "UPDATE remindmes SET content='%s' WHERE title='%s' " % (remindme.get_content(), remindme.get_title(),)
            self.__cursor.execute(sql)
            self.__db.commit()
            return True
        except Exception as err:
            self.__db.rollback()
            return False

    def remove_remindme(self, remindme):
        '''Remove remindme from this repository.'''
        if remindme in self.__deleted_remindmes:
            return False
        try:
            sql = 'DELETE FROM remindmes WHERE title == "{0}" '
            sql = sql.format(remindme.get_title())
            self.__cursor.execute(sql)
            self.__db.commit()
            self.__deleted_remindmes.append(remindme)
            self.__filter_out_deleted()
            return True
        except:
            self.__db.rollback()
            return False

    def remove_remindmes(self):
        '''Removes all remindmes from this repository.'''
        for remindme in self.__remindmes:
            status = self.remove_remindme(remindme)
            if status is False:
                return False
        return True

    def __filter_out_deleted(self):
        '''Filters out deleted remindmes.'''
        self.__remindmes = [r for r in self.__remindmes
            if r not in self.__deleted_remindmes]

    def get_remindmes(self):
        '''Return remindmes from database.'''
        return self.__remindmes

    def save_remindmes(self):
        '''Save all remindmes.'''
        for remindme in self.__remindmes:
            remindme.save()

    def find(self, qualify):
        '''Search through the remindmes.'''
        return [x for x in self.__remindmes if qualify(x)]

    def find_by_title(self, title):
        '''Find the remindme by title.'''
        found = self.find(lambda remindme: remindme.get_title() == title)
        return found[0] if found else None

    def count(self):
        return len(self.get_remindmes())
