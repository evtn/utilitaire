from typing import Iterable
import unicodedata


def get_char_class(char: str):
    if char.isalpha():
        return "alpha"

    if char.isnumeric():
        return "numeric"

    return "other"


def joinlist[E, S](strings: Iterable[E], sep: S) -> Iterable[E | S]:
    i = 0

    for string in strings:
        if i:
            yield sep

        yield string

        i += 1


def get_plain_chars(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if c.isalnum() or c.isspace()
    )
