#!/usr/bin/env python3

import os
import sqlite3

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
    return "2022-05-24"

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
            cur.execute('CREATE TABLE activity_log (date TEXT, active_minutes INTEGER)')
            self.connection.commit()

    def get_activity(self, day):
        """Gets activity for `day`. Returns (date, activive_time_in_minutes)
        if activity was previously recorded for the day. Returns None
        if no activity was logged for the day."""
        cur = self.connection.cursor()
        t = ('2022-05-24',)
        cur.execute('SELECT * FROM activity_log where date=?', t)
        activity = cur.fetchone()
        return activity

    def add_activity(self, minutes):
        """Increases the amount of time logged for today.
        Returns total amount of activity for the day."""
        previous_activity_entry = self.get_activity(today())  # TODO

        cur = self.connection.cursor()
        if not previous_activity_entry:
            t = (today(), minutes)  # TODO
            cur.execute('INSERT INTO activity_log VALUES (?, ?)', t)
            self.connection.commit()
            return minutes

        previous_activity = previous_activity_entry[1]
        total_activity = previous_activity + minutes
        t = (total_activity, today())  # TODO
        cur.execute('UPDATE activity_log SET active_minutes = ? where date = ?', t)
        self.connection.commit()
        return total_activity
