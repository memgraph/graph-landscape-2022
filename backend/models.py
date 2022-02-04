from enum import unique
from typing import Optional
from app import memgraph
from gqlalchemy import Node, Field, Relationship


class Technology(Node):
    name: str = Field(exists=True, unique=True, db=memgraph)
    description: str = Field()
    website: str = Field()
    logo_url: str = Field()


class Organization(Node):
    name: str = Field(exists=True, unique=True, db=memgraph)
    logo_url: str = Field()


class Category(Node):
    name: str = Field(exists=True, unique=True, index=True, db=memgraph)


class IsPartOf(Relationship, type="IS_PART_OF"):
    pass


class BelongsTo(Relationship, type="BELONGS_TO"):
    pass
