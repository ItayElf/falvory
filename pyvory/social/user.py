from dataclasses import dataclass
from typing import List


@dataclass
class User:
    """Represents userdata of a user without auth data"""
    name: str
    bio: str
    link: str
    followers: List[str]  # usernames
    following: List[str]  # usernames
    posts: List[int]  # post ids
    cookbooks: List[int]  # cookbooks ids
