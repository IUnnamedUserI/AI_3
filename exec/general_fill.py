#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Generator

from base_depth import Problem
from base_depth import depth_first_recursive_search as dfs


class FloodFill(Problem):
    def __init__(
        self, start: tuple[int, int], matrix: list[list[str]],
        target: str, fill: str
    ) -> None:
        super().__init__(start, None)
        self.grid = deepcopy(matrix)
        self.target = target
        self.fill = fill

    def actions(self, position: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < len(self.grid) and
                0 <= nc < len(self.grid[0]) and
                self.grid[nr][nc] == self.target):
                yield nr, nc

    def result(self, state: tuple[int, int], action: tuple[int, int]) -> tuple[int, int]:
        self.grid[action[0]][action[1]] = self.fill
        return action


def flood_fill(
    start: tuple[int, int], matrix: list[list[str]],
    target: str, fill: str
) -> list[list[str]]:
    problem = FloodFill(start, matrix, target, fill)
    dfs(problem)
    return problem.grid


if __name__ == "__main__":
    data = [
        list("YYYGGGGGGG"),
        list("YYYYYYGXXX"),
        list("GGGGGGGXXX"),
        list("WWWWWGXGXX"),
        list("WRRRRRGXXX"),
        list("WWWGRRGXXX"),
        list("WBWRRRRRRX"),
        list("WBBBBRRXXX"),
        list("WBBXBBBX.X"),
        list("WBBXXXXXXX"),
    ]

    print("Заменяем 'X' на 'C':")
    filled_grid = flood_fill((3, 9), data, "X", "C")
    for line in filled_grid:
        print(" ".join(line))

    print("\nЗаменяем 'G' на 'V':")
    filled_grid = flood_fill((0, 3), data, "G", "V")
    for line in filled_grid:
        print(" ".join(line))
