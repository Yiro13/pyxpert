from __future__ import annotations


class Node:
    def __init__(self, fact: str, status=None) -> None:
        self.fact = fact
        self.status = status
        self.next: Node | None = None
        self.ant = []

    def link(self, dest: Node) -> None:
        self.next = dest
        dest.ant.append(self)
