#!/usr/bin/env python3

import os
import sqlite3
from datetime import date
from statistics import mean
from time import time

from plover_dojo.wikipedia_word_frequency.word_frequency_list_manager import get_word_frequency_list_as_map

connection = None

HOME = os.environ['HOME']
DB_DIR = os.path.join(HOME, ".dojo")
DB_FILE = os.path.join(DB_DIR, "dojo.db")


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
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


class ActivityLog:
    def __init__(self):
        self.connection = get_connection()
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT * FROM activity_log LIMIT 1')
            cur.fetchone()
        except sqlite3.OperationalError:
            cur.execute('CREATE TABLE activity_log (date TEXT, active_seconds INTEGER)')
            self.connection.commit()

    def get_activity(self, day):
        """Gets activity for `day`. Returns (date, activive_time_in_seconds)
        if activity was previously recorded for the day. Returns None
        if no activity was logged for the day."""
        cur = self.connection.cursor()
        t = (day,)
        cur.execute('SELECT * FROM activity_log where date=?', t)
        activity = cur.fetchone()
        return activity

    def add_activity(self, seconds):
        """Increases the amount of time logged for today.
        Returns total amount of activity for the day."""
        previous_activity_entry = self.get_activity(today())

        cur = self.connection.cursor()
        if not previous_activity_entry:
            t = (today(), seconds)
            cur.execute('INSERT INTO activity_log VALUES (?, ?)', t)
            self.connection.commit()
            return seconds

        previous_activity = previous_activity_entry[1]
        total_activity = previous_activity + seconds
        t = (total_activity, today())
        cur.execute('UPDATE activity_log SET active_seconds = ? where date = ?', t)
        self.connection.commit()
        return total_activity


class StrokeEfficiencyLog:
    def __init__(self):
        self.connection = get_connection()
        StrokeEfficiencyLogInitializer().initialize()

    def add_stroke(self, word, stroke_duration, timestamp=None):
        """Note how long a stroke took. If `timestamp` is omitted,
        method uses the current time.

        Returns True if entry was added successfully, False
        otherwise."""
        cur = self.connection.cursor()
        t = (timestamp or time(), stroke_duration, word)
        try:
            cur.execute("""INSERT INTO Strokes(word_id, timestamp, stroke_duration)
                            SELECT Words.word_id, ?, ?
                            FROM Words
                            WHERE Words.word = ? LIMIT 1""", t)
            self.connection.commit()
            return True
        except Exception:
            return False

    def get_average_speed_and_frequency_for_stroked_words(self):
        cur = self.connection.cursor()
        cur.execute("""SELECT Words.word,
                              Words.frequency,
                              AVG(Strokes.stroke_duration) as AverageDuration
                         FROM Words
                         JOIN Strokes ON Words.word_id = Strokes.word_id
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
            cur.execute("""CREATE TABLE Words (word_id INTEGER PRIMARY KEY,
                                               word TEXT,
                                               frequency INTEGER)""")
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
            cur.execute("""CREATE TABLE Strokes (stroke_id INTEGER PRIMARY KEY,
                                                 word_id INT,
                                                 timestamp REAL,
                                                 stroke_duration REAL,
                                                 FOREIGN KEY(word_id) REFERENCES Words(word_id))""")
            cur.execute('CREATE INDEX StrokedWordIndex ON Strokes(word_id)')
            self.connection.commit()

    def _populate_words_table(self):
        word_frequency_map = get_word_frequency_list_as_map()
        cur = self.connection.cursor()
        for word, frequency in word_frequency_map.items():
            t = (word, frequency)
            cur.execute('INSERT INTO Words (word, frequency) VALUES (?, ?)', t)
        self.connection.commit()
