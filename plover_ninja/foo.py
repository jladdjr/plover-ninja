#!/usr/bin/env python3

import storage

log = storage.ActivityLog()

print(log.get_activity('foo day'))
print(log.add_activity(5))
