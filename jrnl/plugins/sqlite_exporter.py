import os
import sqlite3
from typing import TYPE_CHECKING
from typing import Dict

from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg

if TYPE_CHECKING:
    from jrnl.Entry import Entry
    from jrnl.Journal import Journal


class SqliteExporter:
    """This Exporter can convert entries and journals into text files."""

    names = ["sqlite", "sqlite3"]
    extension = "db"


    @classmethod
    def export_entry(cls, entry: "Entry") -> str:
        """Returns a string representation of a single entry."""
        return str(entry)

    @staticmethod
    def create_schema(path: str) -> None:
        with sqlite3.connect(path) as con: 
            cur = con.cursor()
            tags_table_statement = """
                CREATE TABLE tags (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    tag varchar[32]
                ); 
            """
            cur.execute(tags_table_statement)

            entry_table_statement = """
                CREATE TABLE entries (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title varchar[256], 
                    body text,
                    datetime DATETIME, 
                    starred BOOLEAN
                );             
            """
            cur.execute(entry_table_statement)

            entry_tags_table_statement = """
                CREATE TABLE entry_tags (
                    RELATIONSHIP_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    tag_id integer, 
                    entry_id integer, 
                    FOREIGN KEY(tag_id) REFERENCES tag(ID), 
                    FOREIGN KEY(entry_id) REFERENCES entry(ID)
                ); 
            """
            cur.execute(entry_tags_table_statement)
        
    
    @staticmethod 
    def export_tags(journal: "Journal", path: str) -> Dict[str, int]:
        tags = journal.tags
        tag_map = {} 

        with sqlite3.connect(path) as con: 
            cur = con.cursor() 
            for tag in tags: 
            
                cur.execute("insert into tags (tag) VALUES (?)", (tag.name, ))
                tag_map[tag.name] = cur.lastrowid
            con.commit() 
        return tag_map

    @staticmethod 
    def export_entries(journal: "Journal", tag_map: Dict[str, int], path: str) -> None:
        with sqlite3.connect(path) as con: 
            cur = con.cursor() 
            for entry in journal.entries:
                cur.execute("insert into entries (title, body, datetime, starred) values (?, ?, ?, ?)", 
                (entry.title, entry.body, entry.date, entry.starred))
                entry_id = cur.lastrowid
                entry_tags = entry.tags 
                values = [(tag_map[tag], entry_id) for tag in entry_tags]
                cur.executemany("insert into entry_tags (tag_id, entry_id) values (?, ?)", values)





    @classmethod
    def export(cls, journal: "Journal", output: str | None = None) -> str:
        """Exports to a database file"""
        if output is None or os.path.exists(output):   
            raise Exception("expecting a path to a non-existing file")         


        SqliteExporter.create_schema(output)
        tag_map = SqliteExporter.export_tags(journal, output)
        SqliteExporter.export_entries(journal, tag_map, output)

        print_msg(
            Message(
                MsgText.JournalExportedTo,
                MsgStyle.NORMAL,
                {
                    "path": output,
                },
            )
        )         
        return ""