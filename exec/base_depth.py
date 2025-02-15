#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq
import math
from collections import deque
from typing import Any, Generator


class Problem:
    def __init__(self, initial: Any = None,
                 goal: Any = None, **kwargs) -> None:
        self.initial = initial
        self.goal = goal
        self.__dict__.update(kwargs)

    def actions(self, state: Any) -> Generator:
        raise NotImplementedError

    def result(self, state: Any, action: Any) -> Any:
        raise NotImplementedError

    def is_goal(self, state: Any) -> bool:
        return state == self.goal

    def action_cost(self, s: Any, a: Any, s1: Any) -> int:
        return 1

    def h(self, node: "Node") -> int:
        return 0

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.initial!r}, {self.goal!r})"


class Node:
    def __init__(self, state: Any, parent: "Node" = None,
                 action: Any = None, path_cost: float = 0) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self) -> str:
        return f"<{self.state}>"

    def __len__(self) -> int:
        return 0 if self.parent is None else 1 + len(self.parent)

    def __lt__(self, other: "Node") -> bool:
        return self.path_cost < other.path_cost


failure = Node("failure", path_cost=math.inf)
cutoff = Node("cutoff", path_cost=math.inf)


def expand(problem: Problem, node: Node) -> Generator[Node, None, None]:
    state = node.state
    for action in problem.actions(state):
        next_state = problem.result(state, action)
        cost = node.path_cost + problem.action_cost(state, action, next_state)
        yield Node(next_state, node, action, cost)


def path_actions(node: Node) -> list:
    elsereturn = path_actions(node.parent) + [node.action]
    return [] if node.parent is None else elsereturn


def path_states(node: Node) -> list:
    elsereturn = path_states(node.parent) + [node.state]
    return [] if node in (cutoff, failure, None) else elsereturn


FIFOQueue = deque
LIFOQueue = list


class PriorityQueue:
    def __init__(self, items=(), key=lambda x: x) -> None:
        self.key = key
        self.items = []
        for item in items:
            self.add(item)

    def add(self, item: Any) -> None:
        heapq.heappush(self.items, (self.key(item), item))

    def pop(self) -> Any:
        return heapq.heappop(self.items)[1]

    def top(self) -> Any:
        return self.items[0][1]

    def __len__(self) -> int:
        return len(self.items)


def is_cycle(node: Node) -> bool:
    visited_states = set()
    while node:
        if node.state in visited_states:
            return True
        visited_states.add(node.state)
        node = node.parent
    return False


def depth_first_recursive_search(problem: Problem, node: Node = None) -> Node:
    if node is None:
        node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node
    if is_cycle(node):
        return failure
    for child in expand(problem, node):
        result = depth_first_recursive_search(problem, child)
        if result:
            return result
    return failure
