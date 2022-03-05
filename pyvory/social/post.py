from dataclasses import dataclass
from typing import List

from pyvory.recipes.recipe import Recipe
from pyvory.social import Comment


@dataclass
class Post:
    """Represents a post of a recipe"""
    poster: str  # name of the user who posted
    recipe: Recipe
    comments: List[Comment]
    likes: List[str]  # name of the users who liked
    cooked: List[str]  # name of the users who cooked
    timestamp: int  # int(time.time())
