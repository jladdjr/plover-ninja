#!/usr/bin/env python3

import os
import sqlite3
from datetime import date

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
