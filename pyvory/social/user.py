from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    """Represents userdata of a user without auth data"""
    name: str
    bio: str
    link: str
    followers: List[str]  # names
    following: List[str]  # names
    posts: List[int]  # post ids
    cookbooks: List[int]  # cookbooks ids
    idx: Optional[int] = None

    @classmethod
    def from_tup(cls, tup) -> User:
        def _parse_concat(concat: str | None):
            if concat:
                try:
                    return list({int(v) for v in concat.split(",")})
                except ValueError:
                    return list({v for v in concat.split(",")})
            else:
                return []

        idx, name, bio, link, followings, followers, posts, cookbooks = tup
        followings = _parse_concat(followings)
        followers = _parse_concat(followers)
        posts = _parse_concat(posts)
        cookbooks = _parse_concat(cookbooks)
        return cls(name, bio, link, followers, followings, posts, cookbooks, idx)
