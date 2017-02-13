"""
Utils functions for blueprints methods
"""


def get_boolean(value):
    """
    to get boolean values from query strings

    :param value:
    :return: boolean
    """
    if isinstance(value, bool):
        return value

    if not value:
        return False
    value = value.lower()
    if value in ('false', 'no', 'off', 'n', '0',):
        return False
    if value in ('true', 'yes', 'on', 'y', '1',):
        return True

    return False
