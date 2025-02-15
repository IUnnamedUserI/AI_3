#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Generator

from base_depth import Problem
from base_depth import depth_first_recursive_search as dfs


class LenProblem(Problem):
    def __init__(
        self,
        initial: tuple[int, int] | None,
        goal: tuple[int, int] | None,
        matrix: list[list[str]],
        start: str,
    ) -> None:
        super().__init__(initial, goal)
        self.matrix = matrix
        self.max_len = 0
        self.start = start

    def actions(self, state: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
        found = False
        r, c = state
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < len(self.matrix)
                and 0 <= nc < len(self.matrix[0])
                and ord(self.matrix[nr][nc]) - ord(self.matrix[r][c]) == 1
            ):
                yield nr, nc
                found = True

        if not found:
            length = ord(self.matrix[r][c]) - ord(self.start)
            self.max_len = max(self.max_len, length)

    def result(
        self, state: tuple[int, int], action: tuple[int, int]
    ) -> tuple[int, int]:
        return action


def solve(start: str, matrix: list[list[str]]) -> int:
    problem = LenProblem(None, None, matrix, start)

    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == start:
                problem.initial = (i, j)
                dfs(problem)
    return problem.max_len + 1


if __name__ == "__main__":
    matrix1 = [
        ["D", "E", "H", "X", "B"],
        ["A", "O", "G", "P", "E"],
        ["D", "D", "C", "F", "D"],
        ["E", "B", "E", "A", "S"],
        ["C", "D", "Y", "E", "N"],
    ]

    print(solve("B", matrix1), "символов (старт с символа B)")

    matrix2 = [
        ["A", "B", "C", "H", "E", "F"],
        ["P", "Q", "A", "S", "T", "G"],
        ["L", "B", "W", "V", "U", "H"],
        ["N", "M", "L", "K", "K", "I"],
    ]

    print(solve("V", matrix2), "символов (старт с символа V)")
