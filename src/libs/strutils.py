# Licensed under the LGPL 3.0 License.
# simplepylibs by numlinka.
# strutils

__name__ = "strutils"
__version__ = "1.0"
__author__ = "numlinka"
__license__ = "LGPL 3.0"
__copyright__ = "Copyright (C) 2022 numlinka"

version = (1, 0)


def escape_character_recognition(value: str) -> str:
    """
    ## escape character recognition
    ## 转义字符识别

    Find escape characters in a string and replace them
    with their corresponding special characters.

    找到字符串中的转义字符并替换为其对应的特殊字符.
    """
    table = {
        "n": "\n",
        "t": "\t",
        "r": "\r",
        "\\": "\\",
    }

    keyword = "\\"
    length = len(keyword)
    not_found = -1

    _input = value
    output = ""

    while True:
        result = _input.find(keyword)
        if result == not_found:
            output += _input
            break

        output += _input[:result]
        _input = _input[result+length:]

        if not _input:
            output += keyword
            break

        if _input[0] not in table:
            output += keyword
            continue

        output += table[_input[0]]
        _input = _input[1:]

    return output


__all__ = [
    "escape_character_recognition",
]
