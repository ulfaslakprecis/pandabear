import dataclasses
from typing import Any


@dataclasses.dataclass
class Field:
    typ: Any = None

    # Pandas Series checks
    ge: float = None
    gt: float = None
    lt: float = None
    le: float = None
    isin: list = None
    notin: list = None
    str_contains: str = None
    str_endswith: str = None
    str_startswith: str = None
    notnull: bool = None
    null: bool = None

    # Column name checks
    alias: str = None
    regex: bool = False


@dataclasses.dataclass
class BaseConfig:
    strict: bool | str = True
    multiindex_strict: bool = True
    multiindex_ordered: bool = False
    multiindex_unique: bool = True

    @classmethod
    def _override(cls, other_cls):
        return type('SchemaConfig', (other_cls, cls), {})