# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
import logging
from typing import Dict

from jrnl.encryption.BaseEncryption import BaseEncryption

SHIFT_CODE_DIST = 3

def make_caesar_transtable() -> Dict[int, int|None]:
    from_small_letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    to_small_letters = from_small_letters[SHIFT_CODE_DIST:] +  from_small_letters[:SHIFT_CODE_DIST]

    from_cap_letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    to_cap_letters = from_cap_letters[SHIFT_CODE_DIST:] +  from_cap_letters[:SHIFT_CODE_DIST]
    
    table = str.maketrans(str(from_small_letters + from_cap_letters), str(to_small_letters + to_cap_letters))
    return table

enc_table = make_caesar_transtable()
dec_table = {v:k for k, v in enc_table.items()}

class CaesarEncryption(BaseEncryption):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.debug("start")

    def _encrypt(self, text: str) -> bytes:
        logging.debug("encrypting")
        text = text.translate(enc_table) 
        return text.encode(self._encoding)

    def _decrypt(self, text: bytes) -> str:
        logging.debug("decrypting")
        text_str = text.decode(self._encoding)
        text_str = text_str.translate(dec_table)  
        return text_str 
