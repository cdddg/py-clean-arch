import strawberry

from core.type import UUIDStr


@strawberry.scalar(description=UUIDStr.__doc__)
class UUIDStrScalar:
    @staticmethod
    def serialize(value: UUIDStr) -> str:
        return str(value)

    @staticmethod
    def parse_value(value: str) -> UUIDStr:
        return UUIDStr(value)
