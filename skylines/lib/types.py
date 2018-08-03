import sys


def is_int(number):
    if sys.version_info[0] == 2:
        return isinstance(number, (int, long))
    else:
        return isinstance(number, int)


def is_string(value):
    if sys.version_info[0] == 2:
        return isinstance(value, (str, unicode))
    else:
        return isinstance(value, (bytes, str))