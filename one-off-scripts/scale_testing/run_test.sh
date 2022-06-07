#!/bin/bash

rm -rf test.db
cp test.db.orig test.db

./scale_test.py
