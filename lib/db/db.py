# check if file exists on system
from os.path import isfile
from sqlite3 import connect
from apscheduler.triggers.cron import CronTrigger

# database constant
DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


@with_commit
def build():
    # if our sql build file exists we need to scriptexec
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)


def commit():
    # print("Committing...")
    cxn.commit()


def autosave(sched):
    sched.add_job(commit, CronTrigger(second=0))
    # add job to scheduler to commit to database every time second value
    # ticks to 0 - e.g every minute


def close():
    cxn.close()


def field(command, *values):
    cur.execute(command, tuple(values))
    # if row exists get first element since its a tuple
    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()


def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()


def column(command, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    cur.execute(command, tuple(values))


# faster than doing a bunch of execute statements
def multiexec(command, valueset):
    cur.executemany(command, valueset)


    # load the script and do everything in there
def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())
