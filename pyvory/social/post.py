from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

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
    idx: Optional[int] = None

    @classmethod
    def from_tup(cls, tup) -> Post:
        recipe = Recipe.from_tup(tup[1:11])
        comments = list(sorted(
            {Comment.from_tup(t) for t in
             zip(tup[11].split("~"), tup[12].split("~"), tup[13].split("~"), tup[14].split("~"))},
            key=lambda x: x.timestamp, reverse=True)) if tup[
            11] else []
        likes = list({v for v in tup[15].split("~")}) if tup[15] else []
        cooked = list({v for v in tup[16].split("~")}) if tup[16] else []
        return cls(tup[0], recipe, comments, likes, cooked, tup[17], tup[18])
