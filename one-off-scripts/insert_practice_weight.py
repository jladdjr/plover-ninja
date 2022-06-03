#!/usr/bin/env python3

import math
import sqlite3

conn = sqlite3.connect('/home/jim/.plover_ninja/ninja.db')

def log(t):
    return math.log(t, 1.88265)
conn.create_function('log', 1, log)

cur = conn.cursor()
cur.execute('Update Words SET practice_weight = log(frequency)')
conn.commit()
