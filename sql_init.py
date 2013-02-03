#!/usr/bin/python
# -*- coding: utf-8 -*-
# SQLite initialization module
import sqlite3 as lite
import sys

con = lite.connect('customerio.db')

with con:

    cur = con.cursor()
    cur.execute("CREATE TABLE Emails(Id INTEGER PRIMARY KEY AUTOINCREMENT, Email TEXT)")
