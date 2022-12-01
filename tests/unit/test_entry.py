from jrnl.Entry import Entry


def test_delete_tag(request):
    text = "@tag at the begining of the text + @tagnot is not a @tag, and one at the end: @tag"
    res = Entry.remove_tag_from_string(text, "tag", "@#")
    assert res == "tag at the begining of the text + @tagnot is not a tag, and one at the end: tag"

def test_delete_tag_after_period(request):
    """Tags must be preceeded by space, or be at the beginning of the line"""
    text = "@tag at the begining of the text.@tag again"
    res = Entry.remove_tag_from_string(text, "tag", "@#")
    assert res == "tag at the begining of the text.@tag again"

def test_delete_tag_multiline(request):
    text = """@tag at the begining of the text + @tagnot is not a @tag, and one at the end: @tag\n
            @tag at the begining of the text + @tagnot is not a @tag, and one at the end: @tag"""

    expected = """tag at the begining of the text + @tagnot is not a tag, and one at the end: tag\n
            tag at the begining of the text + @tagnot is not a tag, and one at the end: tag"""

    res = Entry.remove_tag_from_string(text, "tag", "@#")
    assert res == expected
