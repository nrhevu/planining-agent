from __future__ import annotations
from typing import List
from difflib import get_close_matches
from .base import MemoryStore

class InMemoryStore(MemoryStore):
    def __init__(self):
        self._items: List[str] = []

    def add(self, text: str) -> None:
        self._items.append(text)

    def search(self, query: str, k: int = 5) -> List[str]:
        return get_close_matches(query, self._items, n=k, cutoff=0.0)
