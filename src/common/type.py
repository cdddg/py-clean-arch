import re


class UUIDStr(str):
    """
    UUID represented as a hexadecimal string.
    """

    # regular expression to match 32 hexadecimal characters

    UUID_PATTERN = re.compile(r'^[a-fA-F0-9]{32}$')

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)

        if not cls.UUID_PATTERN.match(instance):
            raise ValueError(f'\'{instance}\' is not a valid UUID hexadecimal string')

        return instance
