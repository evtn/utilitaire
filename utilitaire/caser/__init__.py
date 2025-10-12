from typing_extensions import Iterable

from utilitaire.stringops import get_char_class


def get_words(key: str, force_sep: str | None = None) -> Iterable[str]:
    if not key:
        return []

    buf: list[list[str]] = [[]]

    def add_word(*start_chars: str):
        if buf[-1]:
            buf.append(list(start_chars))
        elif start_chars:
            buf[-1].extend(start_chars)

    for i, char in enumerate(key):
        current_word = buf[-1]
        char_class = get_char_class(char)

        last_char = key[i - 1]
        last_char_class = get_char_class(last_char)

        if char_class == "other":
            if force_sep is not None:
                char = force_sep

            if last_char_class != "other":
                add_word(char)
            else:
                current_word.append(char)
            continue

        if last_char_class == "other":
            add_word()
            current_word = buf[-1]

        if (
            last_char_class == "alpha"
            and last_char.isupper()
            and char.islower()
            and not current_word
        ):
            current_word.append(buf[-2].pop())

        if not current_word or last_char_class == "other":
            current_word.append(char)
            continue

        if char_class != last_char_class:
            add_word(char)
            continue

        if char_class == "alpha":
            is_lower = char.islower()
            is_last_lower = last_char.islower()

            # current upper
            if not is_lower:
                # last lower
                if is_last_lower:
                    add_word(char)
                    continue

                # last upper
                current_word.append(char)
                continue

            # current lower

            if not is_last_lower:
                if len(current_word) > 1:
                    add_word(current_word.pop(), char)
                    continue

        current_word.append(char)

    return filter(None, ("".join(word) for word in buf))


_EXAMPLES = [
    "kebab-case",
    "snake_case",
    "PascalCase",
    "XHTMLRequest",
    "UserID",
]


def _make_docstring(converter):
    return "\n".join(" -> ".join([ex, converter(ex)]) for ex in _EXAMPLES)


class Case:
    @staticmethod
    def snake(key: str):
        """
        ```
        kebab-case -> kebab_case
        snake_case -> snake_case
        PascalCase -> pascal_case
        XHTMLRequest -> xhtml_request
        UserID -> user_id
        ```
        """

        return "_".join(word.lower() for word in get_words(key, force_sep=""))

    @staticmethod
    def kebab(key: str):
        """
        ```
        kebab-case -> kebab-case
        snake_case -> snake-case
        PascalCase -> pascal-case
        XHTMLRequest -> xhtml-request
        UserID -> user-id
        ```
        """
        return "-".join(word.lower() for word in get_words(key, force_sep=""))

    @staticmethod
    def camel(key: str, cap_first: bool = False):
        """
        ```
        kebab-case -> kebabCase
        snake_case -> snakeCase
        PascalCase -> pascalCase
        XHTMLRequest -> xhtmlRequest
        UserID -> userId
        ```

        *for cap_first=True, check out pascal_case docstring
        """

        words = list(get_words(key, force_sep=""))

        if not words:
            return ""

        first_word = words[0].lower()

        if cap_first:
            first_word = first_word.capitalize()

        buf: list[str] = [first_word]

        last_class = get_char_class(words[0][-1])

        for word in words[1:]:
            next_class = get_char_class(word[0])

            if next_class == "numeric" and last_class == "numeric":
                buf.append("_")

            last_class = get_char_class(word[-1])

            buf.append(word.lower().capitalize())

        return "".join(buf)

    @staticmethod
    def pascal(key: str) -> str:
        """
        ```
        kebab-case -> KebabCase
        snake_case -> SnakeCase
        PascalCase -> PascalCase
        XHTMLRequest -> XhtmlRequest
        UserID -> UserId
        ```
        """
        return Case.camel(key, cap_first=True)
