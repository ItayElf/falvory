from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Comment:
    """Represents a comment commented on a post"""
    commenter: str  # name of the user
    content: str
    timestamp: int  # int(time.time())

    @classmethod
    def from_tup(cls, tup) -> Comment:
        return cls(*tup)
