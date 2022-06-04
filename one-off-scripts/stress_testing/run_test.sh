#!/bin/bash

rm -rf test.db
cp test.db.orig test.db

./stress_test.py

cp ~/git/plover-ninja/one-off-scripts/test.db ~/.plover_ninja/ninja.db
