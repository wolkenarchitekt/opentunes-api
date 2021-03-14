import json
from decimal import Decimal

from sqlalchemy import TypeDecorator
from sqlalchemy.types import Integer, Numeric, String


class ArrayType(TypeDecorator):
    """ Custom Array Type for SQLite (not necessary for Postgres) """

    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return ArrayType(self.impl.length)


class SqliteNumeric(TypeDecorator):
    impl = Integer

    def __init__(self, scale):
        TypeDecorator.__init__(self)
        self.scale = scale
        self.multiplier_int = 10 ** self.scale

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = int(Decimal(value) * self.multiplier_int)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = Decimal(value) / self.multiplier_int
        return value


class DBAgnosticNumeric(TypeDecorator):
    """
    Use NUMERIC type on Postgres, use Integer on SQLite
    """

    impl = Numeric

    def load_dialect_impl(self, dialect):
        if dialect.name == "sqlite":
            return dialect.type_descriptor(SqliteNumeric(scale=6))
        return self.impl
