from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str
    email: str
    first_name: str
    last_name: str


@dataclass
class Tag:
    id: int
    name: str
    color: str
    slug: str

@dataclass
class Recipe:
    pass
