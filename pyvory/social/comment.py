from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Comment:
    """Represents a comment commented on a post"""
    commenter: str  # name of the user
    content: str
    timestamp: int  # int(time.time())
    idx: Optional[int] = None

    @classmethod
    def from_tup(cls, tup) -> Comment:
        return cls(tup[0], tup[1], int(tup[2]), int(tup[3]))
