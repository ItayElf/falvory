from dataclasses import dataclass

from pyvory.social import User


@dataclass
class Comment:
    """Represents a comment commented on a post"""
    commenter: User
    content: str
    timestamp: int  # int(time.time())
