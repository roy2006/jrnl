from jrnl.encryption.CaesarEncryption import make_caesar_transtable


def test_make_caesar_transtable(request):
    table = make_caesar_transtable()

    assert table[ord('a')] == ord('d') 
    assert table[ord('A')] == ord('D') 

    assert table[ord('y')] == ord('b') 
    assert table[ord('Y')] == ord('B')     