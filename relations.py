from dataclasses import dataclass


@dataclass
class Relation:
    name: str
    columns = []
    foreign_keys = []


@dataclass
class _ColumnConstraints:
    is_part_of_key: bool
    nullable: bool
    unique: bool


@dataclass
class Column(_ColumnConstraints):
    name: str
    type: str


@dataclass
class ForeignKey(_ColumnConstraints):
    referenced_table_name: str
