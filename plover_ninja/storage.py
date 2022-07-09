#!/usr/bin/env python3

import math
import os
import sqlite3
import tempfile
import threading
from datetime import date
from pathlib import Path
from uuid import uuid4

from plover_ninja.wikipedia_word_frequency.word_frequency_list_manager import get_word_frequency_list_as_map

connection = None

HOME = str(Path.home())
TEMP_DIR = tempfile.gettempdir()
DB_DIR = os.path.join(HOME, ".plover_ninja")
DB_FILE = os.path.join(DB_DIR, "ninja.db")  # os.path.join returns a string


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    db_file = Path(DB_FILE)
    if not db_file.is_file():
        db_file.touch()
        db_file.chmod(0o700)  # Octal: 700
    global connection
    if not connection:
        connection = sqlite3.connect(DB_FILE)
    return connection


def close_connection():
    global connection
    if connection:
        connection.close()
        connection = None


def today():
    d = date.today()
    return d.strftime("%Y-%m-%d")


class SettingsManager:
    def __init__(self):
        self.connection = get_connection()
        self._ensure_tables_exists()

    def _ensure_tables_exists(self):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT * FROM Settings LIMIT 1')
            cur.fetchone()
        except sqlite3.OperationalError:
            cur.execute("""CREATE TABLE Settings (setting_id INTEGER PRIMARY KEY,
                                                  name TEXT,
                                                  value TEXT)""")
            self.connection.commit()

    def get_setting(self, name):
        """Returns setting if found, otherwise returns `None`"""
        cur = self.connection.cursor()
        t = (name,)
        cur.execute("""SELECT value FROM Settings
                       WHERE name = ?""", t)
        res = cur.fetchone()
        if res is None:
            return None
        return res[0]

    def setting_exists(self, name):
        return self.get_setting(name) is not None

    def set_setting(self, name, value):
        cur = self.connection.cursor()
        if self.setting_exists(name):
            t = (value, name)
            cur.execute("""UPDATE Settings
                           SET value = ?
                           WHERE name = ?""", t)
        else:
            t = (name, value)
            cur.execute("""INSERT INTO Settings(name, value)
                           VALUES (?, ?)""", t)
        self.connection.commit()


class StrokeEfficiencyLog:
    def __init__(self):
        self.connection = get_connection()
        self.strokes_since_average_recomputed = 0
        self.avg_stroke_recalculation_thread = None
        StrokeEfficiencyLogInitializer().initialize()

    def add_stroke(self, word, stroke_duration):
        """Note how long a stroke took.

        Returns True if entry was added successfully, False
        otherwise."""
        # Before processing stroke, see if any existing
        # threads for recalculating stroke duration averages
        # have finished
        t = self.avg_stroke_recalculation_thread
        if t is not None and not t.is_alive():
            self.avg_stroke_recalculation_thread = None

        if word is None:
            return

        # Our corpus of words that we used to form the words
        # table is case-insensitive, so the strokes we log
        # will be, too
        word = word.lower()

        cur = self.connection.cursor()
        # sqlite date functions:
        # https://sqlite.org/lang_datefunc.html
        #
        # hex() is a helpful sqlite function for
        # viewing the uuid4 primary key value
        # used for stroke_uuid
        # https://sqlite.org/lang_corefunc.html#hex
        primary_key = uuid4().bytes
        t = (primary_key, stroke_duration, word)
        cur.execute("""INSERT INTO Strokes(stroke_uuid, word_id, date, stroke_duration)
                        SELECT ?, Words.word_id, DATE('now', 'localtime'), ?
                        FROM Words
                        WHERE Words.word = ? LIMIT 1""", t)
        # indicate that average stroke duration needs to
        # be recalculated for this word
        t = (word,)
        cur.execute("""UPDATE Words
                        SET average_stroke_duration_dirty_flag = 1
                        WHERE word = ?""", t)
        self.connection.commit()

        # periodically recompute average stroke duration
        self.strokes_since_average_recomputed += 1

        if self.strokes_since_average_recomputed > 100:
            self.strokes_since_average_recomputed = 0
            # ensure that any existing threads that were
            # started to recompute average stroke duration
            # have finished executing. If they have not, raise
            # an exception as this may be an indication
            # that the thread's task has run into an issue.
            if self.avg_stroke_recalculation_thread is not None:
                error_msg = 'Previous process that was recomputing ' + \
                    'the average stroke duration never closed.\n' + \
                    f'{self.avg_stroke_recalculation_proc.exitcode}'
                # crash hard
                raise Exception(error_msg)
            self.avg_stroke_recalculation_thread = update_average_stroke_duration(blocking=False)
        return True

    def get_average_speed_and_frequency_for_stroked_words(self):
        cur = self.connection.cursor()
        cur.execute("""SELECT Words.word,
                              Words.frequency,
                              AVG(Strokes.stroke_duration) AS AverageDuration
                         FROM Words
                         JOIN Strokes ON Words.word_id = Strokes.word_id
                         GROUP BY Words.word
                         ORDER BY Words.frequency DESC
                    """)
        rows = cur.fetchall()
        return rows


class StrokeEfficiencyLogInitializer:
    # TODO: Make these class methods
    def __init__(self):
        self.connection = get_connection()

    def initialize(self):
        self._ensure_tables_exist()

    def _ensure_tables_exist(self):
        cur = self.connection.cursor()
        # Words table
        try:
            cur.execute('SELECT * FROM Words LIMIT 1')
            cur.fetchone()
        except sqlite3.OperationalError:
            # sqlite does not have a separate boolean data type;
            # INTEGER is used instead
            # https://www.sqlite.org/datatype3.html#boolean_datatype
            cur.execute("""CREATE TABLE Words (word_id INTEGER PRIMARY KEY,
                                               word TEXT,
                                               frequency INTEGER,
                                               practice_weight REAL,
                                               average_stroke_duration REAL DEFAULT NULL,
                                               average_stroke_duration_dirty_flag INTEGER DEFAULT NULL)""")
            cur.execute('CREATE INDEX WordIdIndex ON Words(word_id)')
            cur.execute('CREATE INDEX WordIndex ON Words(word)')
            self.connection.commit()

            # since table didn't exist, need to
            # populate table
            self._populate_words_table()

        # Strokes table
        try:
            cur.execute('SELECT * FROM Strokes LIMIT 1')
            cur.fetchone()
        except sqlite3.OperationalError:
            # Create the Strokes table using `WITHOUT ROWID`
            # in order to prevent the rows from being
            # listed in the order in which they were added
            # by a SELECT statement.
            #
            # https://www.sqlite.org/withoutrowid.html
            cur.execute("""CREATE TABLE Strokes (stroke_uuid BLOB PRIMARY KEY,
                                                 word_id INT,
                                                 date INTEGER,
                                                 stroke_duration REAL,
                                                 FOREIGN KEY(word_id) REFERENCES Words(word_id))
                                                WITHOUT ROWID""")
            cur.execute('CREATE INDEX StrokedWordIndex ON Strokes(word_id)')
            self.connection.commit()

    def _populate_words_table(self):
        def get_practice_weight(t):
            t = int(t)
            return math.log(t, 1.88265334)

        # note that this returns only lower-case words
        word_frequency_map = get_word_frequency_list_as_map()
        cur = self.connection.cursor()
        for word, frequency in word_frequency_map.items():
            t = (word, frequency, get_practice_weight(frequency))
            cur.execute('INSERT INTO Words (word, frequency, practice_weight) VALUES (?, ?, ?)', t)
        self.connection.commit()


###################################################
# Lessons

def get_most_common_words_that_have_not_been_used_yet(num_words=5):
    connection = get_connection()
    cur = connection.cursor()

    t = (num_words, )
    cur.execute("""SELECT word_id, word FROM Words
                   WHERE word_id NOT IN
                     (SELECT word_id FROM Strokes)
                   ORDER BY word_id ASC
                   LIMIT ?""", t)
    words = cur.fetchall()
    return words


def get_rarely_used_words(num_words=10, threshold=100):
    """Returns list of words that have been used less than
    `threshold` number of times. Scans words according
    to their general frequency of use.

    Returns list of tuples where each tuple contains:
    - Count of strokes
    - Word frequency
    - Word
    """
    connection = get_connection()
    cur = connection.cursor()

    t = (num_words, )
    cur.execute("""SELECT COUNT(Strokes.stroke_uuid) AS StrokeCount,
                        Words.word_id,
                        Words.word
                        FROM Strokes
                        JOIN Words ON Strokes.word_id = Words.word_id
                        GROUP BY Strokes.word_id
                        ORDER BY Words.frequency DESC
                        LIMIT ?
                """, t)
    words = cur.fetchall()
    return words


def get_slowest_stroked_words(num_words=10):
    connection = get_connection()
    cur = connection.cursor()

    # update average stroke duration for
    # any words where the `average_stroke_duration_dirty_flag`
    # is TRUE
    update_average_stroke_duration()

    t = (num_words,)
    cur.execute("""SELECT word_id,
                          word,
                          practice_weight,
                          average_stroke_duration,
                          average_stroke_duration * Words.practice_weight AS WeightedDuration
                          FROM Words
                          WHERE NOT average_stroke_duration IS NULL
                          ORDER BY WeightedDuration DESC
                          LIMIT ?
                """, t)
    words = cur.fetchall()
    return words


def _update_average_stroke_duration(db_file, name='no_name'):
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()

    # get list of words where the average needs
    # to be recomputed
    cur.execute("""SELECT word_id
                   FROM WORDS
                   WHERE average_stroke_duration_dirty_flag = 1""")
    res = cur.fetchall()
    word_ids = tuple(t[0] for t in res)

    # calculate average stroke duration
    # There's got to be a better way to SELECT from
    # a dynamic list
    # https://stackoverflow.com/a/5766293
    cur.execute(f"""SELECT word_id, AVG(stroke_duration)
                    FROM Strokes
                    WHERE word_id IN ({','.join(['?']*len(word_ids))})
                    GROUP BY word_id
                """, word_ids)
    res = cur.fetchall()

    # save new averages
    for word_id, avg in res:
        t = (avg, word_id)
        cur.execute("""UPDATE Words
                        SET average_stroke_duration = ?,
                            average_stroke_duration_dirty_flag = 0
                        WHERE word_id = ?""", t)
    # commit results
    connection.commit()
    connection.close()


def update_average_stroke_duration(blocking=True):
    """If blocking is True, will update averages synchronously.

    If `blocking` is False, will return a Thread object that
    has been started.
    """
    if blocking:
        _update_average_stroke_duration(DB_FILE)
        return None

    t = threading.Thread(target=_update_average_stroke_duration, args=(DB_FILE, uuid4()))
    t.start()
    return t


def get_daily_number_of_strokes():
    connection = sqlite3.connect(DB_FILE)
    cur = connection.cursor()

    # get list of words where the average needs
    # to be recomputed
    cur.execute("""SELECT date, count(stroke_uuid)
                   FROM Strokes
                   GROUP BY date
                   ORDER BY Date Desc""")
    res = cur.fetchall()
    return {k: v for k, v in res}
