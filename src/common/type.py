import re


class UUIDStr(str):
    """UUID represented as a hexadecimal string."""

    # regular expression to match 32 hexadecimal characters

    UUID_PATTERN = re.compile(r'^[a-fA-F0-9]{32}$')

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)

        if not cls.UUID_PATTERN.match(instance):
            raise ValueError(f'\'{instance}\' is not a valid UUID hexadecimal string')

        return instance


class PokemonNumberStr(str):
    """Pokemon Number represented as a string in the range "0001" to "9999"."""

    # regular expression to match numbers from 0001 to 9999
    NUMBER_PATTERN = re.compile(r'^\d{4}$')

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)

        if not cls.NUMBER_PATTERN.match(instance) or instance == '0000':
            raise ValueError(
                f'\'{instance}\' is not a valid number string in the range "0001" to "9999"'
            )

        return instance
