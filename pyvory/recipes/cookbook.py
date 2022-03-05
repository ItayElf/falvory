from dataclasses import dataclass
from typing import List, Optional

from pyvory.recipes.section import Section


@dataclass
class Cookbook:
    """Represents a collection of recipes organized into sections"""
    title: str
    creator: str
    sections: List[Section]
    bottom_title: bool
    background_color: str  # hex rgb color with '#'
    font_color: str
    accent_color: Optional[str]
