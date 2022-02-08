from enum import unique
from genericpath import exists
from typing import Optional
from app import memgraph
from gqlalchemy import Node, Field, Relationship


class Company(Node):
    name: str = Field(exists=True, db=memgraph)
    website: str = Field()


class Category(Node):
    name: str = Field(exists=True, unique=True, index=True, db=memgraph)


class Subcategory(Node):
    name: str = Field(exists=True, unique=True, index=True, db=memgraph)


class IsPartOf(Relationship, type="IS_PART_OF"):
    pass


class BelongsTo(Relationship, type="BELONGS_TO"):
    pass
