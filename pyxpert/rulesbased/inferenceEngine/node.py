from __future__ import annotations


class Node:
    def __init__(self, fact: str) -> None:
        self.fact = fact
        self.status = None
        self.ant = []
        self.next = []

    def link(self, dest: Node) -> None:
        self.next = dest
        dest.ant.append(self)
