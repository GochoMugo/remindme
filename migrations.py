'''
Handles migrations from one version to another version.
'''

import os
import sqlite3
import sys
import remindme


CURRENT_VERSION = None
NEW_VERSION = None

console = remindme.utils.Console("migration")
db_file = remindme.config.PATHS["db_file"]


def detect_versions():
    '''Detects the current version installed.'''
    global CURRENT_VERSION
    global NEW_VERSION
    cwd = os.getcwd()
    sys.path.remove(cwd)
    old_mod = sys.modules["remindme"]
    del sys.modules["remindme"]
    try:
        import remindme
        CURRENT_VERSION = remindme.__version__
        console.info("currently installed version: {0}".format(CURRENT_VERSION))
    except:
        console.error("failed to detect currently installed version")
        pass
    sys.path.append(cwd)
    sys.modules["remindme"] = old_mod
    import remindme # we have to re-import here!!!
    NEW_VERSION = remindme.__version__
    console.info("new version to install: {0}".format(NEW_VERSION))


def migrate():
    '''Handles invoking migrations.'''
    console.info("process migrations")
    global CURRENT_VERSION 
    OLD_VERSION = CURRENT_VERSION
    if CURRENT_VERSION == "0.2.1" or CURRENT_VERSION is None:
        CURRENT_VERSION = migrate_1() # 1st ever migration
    if CURRENT_VERSION is None:
        sys.exit(1)
    if OLD_VERSION != CURRENT_VERSION: # there was change/migration
        return migrate()
    console.success("finished migrating")


def migrate_1():
    '''Migrates from 0.2.1 to 0.3.0

    Renames database column, `keywords`, to `title`.
    See "http://stackoverflow.com/questions/805363/how-do-i-rename-a-column-in
    -a-sqlite-database-table" for more information.
    '''
    console.info("migrating from 0.2.1 to 0.3.0")
    sql_rename_orig_tbl = "ALTER TABLE remindmes RENAME TO tmp_remindmes;"
    sql_create_tbl = "CREATE TABLE remindmes(title, content);"
    sql_copy_old_tbl = '''
        INSERT INTO remindmes(title, content) SELECT *
        FROM tmp_remindmes;
    '''
    sql_drop_orig_tbl = "DROP TABLE tmp_remindmes;"
    try:
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        cursor.execute(sql_rename_orig_tbl)
        cursor.execute(sql_create_tbl)
        cursor.execute(sql_copy_old_tbl)
        cursor.execute(sql_drop_orig_tbl)
        db.commit()
        console.success("success migrating from 0.2.1 to 0.3.0")
        return "0.3.0"
    except Exception as err:
        db.rollback()
        console.error("error migrating")
        console.error(err)
        return None


def start():
    '''Start migrations.'''
    detect_versions()
    migrate()


if __name__ == "__main__":
    start()
