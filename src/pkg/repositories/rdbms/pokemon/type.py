from sqlalchemy import String, TypeDecorator

from core.type import UUIDStr


class UUIDStrType(TypeDecorator):  # pylint: disable=abstract-method
    impl = String

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(String(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        return UUIDStr(value)

    @property
    def python_type(self):
        return str
