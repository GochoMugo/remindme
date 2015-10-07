'''
Handles migrations from one version to another version.
'''

import sqlite3
import subprocess
import sys
import remindme


CURRENT_VERSION = None
NEW_VERSION = remindme.__version__
MIGRATIONS = {}

console = remindme.utils.Console("migration")
db_file = remindme.config.PATHS["db_file"]


def detect_version():
    '''Detects the current version installed.'''
    global CURRENT_VERSION
    try:
        # user may not have installed remindme EVER
        version = subprocess.check_output(["remindme", "--version"], stderr=subprocess.STDOUT)
        version = version.strip().strip("remindme ")
        CURRENT_VERSION = version or "unversioned"
        console.info("currently installed version: {0}".format(CURRENT_VERSION))
    except Exception as err:
        console.error("could not detect currently-installed version: %s" % err)
        pass
    console.info("new version to install: {0}".format(NEW_VERSION))


def migrate():
    '''Handles invoking migrations.'''
    console.info("process migrations")
    global CURRENT_VERSION
    func = MIGRATIONS.get(CURRENT_VERSION, None)
    # we did not find a migration strategy so just exit
    if func is None:
        console.success("no more migrations to perform")
        return
    CURRENT_VERSION = func()
    # the previous call sets CURRENT_VERSION to None if it failed!
    if CURRENT_VERSION is None:
        sys.exit(1)
    return migrate()


def migrate_1():
    '''Migrates to 0.3.0

    Renames database column, `keywords`, to `title`.
    See "http://stackoverflow.com/questions/805363/how-do-i-rename-a-column-in
    -a-sqlite-database-table" for more information.
    '''
    console.info("migrating to 0.3.0")
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
        console.success("success migrating to 0.3.0")
        return "0.3.0"
    except Exception as err:
        db.rollback()
        console.error("error migrating")
        console.error(err)
        return None


def migrate_2():
    '''Migrate to 0.5.0'''
    console.info("migrating to 0.5.0")
    sql_rename_orig_tbl = "ALTER TABLE remindmes RENAME TO tmp_remindmes;"
    sql_create_tbl = "CREATE TABLE remindmes(title, content BLOB, salt BLOB);"
    sql_copy_old_tbl = "INSERT INTO remindmes(title, content) SELECT * FROM tmp_remindmes;"
    sql_drop_orig_tbl = "DROP TABLE tmp_remindmes;"
    try:
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        cursor.execute(sql_rename_orig_tbl)
        cursor.execute(sql_create_tbl)
        cursor.execute(sql_copy_old_tbl)
        cursor.execute(sql_drop_orig_tbl)
        db.commit()
        console.success("success migrating to 0.5.0")
        return "0.5.0"
    except Exception as err:
        db.rollback()
        console.error("error migrating")
        console.error(err)
        return None


MIGRATIONS["unversioned"] = migrate_1
MIGRATIONS["0.2.1"] = migrate_1
MIGRATIONS["0.3.0"] = migrate_2
MIGRATIONS["0.4.0"] = migrate_2


def start():
    '''Start migrations.'''
    detect_version()
    migrate()


if __name__ == "__main__":
    start()
