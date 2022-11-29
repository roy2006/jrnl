# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from typing import TYPE_CHECKING
import re 

from jrnl.plugins.text_exporter import TextExporter
from jrnl.plugins.util import get_tags_count

if TYPE_CHECKING:
    from jrnl.Entry import Entry
    from jrnl.Journal import Journal

WORDS_RE = re.compile(r"[a-zA-Z]{5,}")

class BlankWordsExporter(TextExporter):
    """This Exporter can convert entries and journals into json."""

    names = ["blank"]
    extension = "txt"

    @staticmethod
    def blank_transformer(s: str) -> str: 
        def word_transformer(m: re.Match) -> str: 
            if m.group().startswith("@"):
                return m.group() 
            else: 
                return "_" * (m.span()[1] - m.span()[0])
        res = WORDS_RE.sub(word_transformer, s) 
        return res

    @classmethod
    def export_entry(cls, entry: "Entry") -> str:
        if entry.body: 
            entry.body = BlankWordsExporter.blank_transformer(entry.body)
        
        if entry.title:
            entry.title = BlankWordsExporter.blank_transformer(entry.title)
        return str(entry)

    # @classmethod
    # def export_journal(cls, journal: "Journal") -> str:
    #     """Returns a json representation of an entire journal."""
    #     tags = get_tags_count(journal)
    #     result = {
    #         "tags": {tag: count for count, tag in tags},
    #         "entries": [cls.entry_to_dict(e) for e in journal.entries],
    #     }
    #     return json.dumps(result, indent=2)
