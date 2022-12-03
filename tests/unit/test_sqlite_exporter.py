from jrnl.plugins.sqlite_exporter import SqliteExporter
import os
import sqlite3

def test_create_schema(tmp_path):
    path = tmp_path / "test.db"
    SqliteExporter.create_schema(path)
    with sqlite3.connect(path) as con: 
        cur = con.cursor() 
        cur.execute('SELECT name from sqlite_master where type= "table"')
        tables = cur.fetchall() 
        tables = [r[0] for r in tables]
        assert "tags" in tables
        assert "entries" in tables
        assert "entry_tags" in tables
    # SELECT name from sqlite_master where type= "table"
    # print(cursorObj.fetchall())
