#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Generator

from base_depth import Problem
from base_depth import depth_first_recursive_search as dfs

# Вам дана матрица символов размером M × N. Ваша задача — найти и вывести
# список всех возможных слов, которые могут быть сформированы
# из последовательности соседних символов в этой матрице.
# При этом слово может формироваться во всех восьми возможных направлениях
# (север, юг, восток, запад,
# северо-восток, северо-запад, юго-восток, юго-запад),
# и каждая клетка может быть использована в слове только один раз.


class WordsProblem(Problem):
    def __init__(
        self,
        initial: tuple[tuple[int, int], str] | None,
        goal: str | None,
        board: list[list[str]],
        word: str | None,
    ) -> None:
        super().__init__(initial, goal)
        self.board = board
        self.word = word
        self.visited: set[tuple[int, int]] = set()

    def actions(
        self, state: tuple[tuple[int, int], str]
    ) -> Generator[tuple[int, int], None, None]:
        r, c = state[0]
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < len(self.board)
                and 0 <= nc < len(self.board[0])
                and self.word and len(state[1]) < len(self.word)
                and self.board[nr][nc] == self.word[len(state[1])]
                and (nr, nc) not in self.visited
            ):
                self.visited.add((nr, nc))
                yield nr, nc

    def result(
        self, state: tuple[tuple[int, int], str], action: tuple[int, int]
    ) -> tuple[tuple[int, int], str]:
        r, c = action
        return (action, state[1] + self.board[r][c])

    def is_goal(self, state: tuple[tuple[int, int], str]) -> bool:
        return self.word is not None and state[1] == self.word


def solve(board: list[list[str]], dictionary: list[str]) -> set[str]:
    words = set()
    for word in dictionary:
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == word[0]:
                    problem = WordsProblem(((i, j), word[0]), word, board, word)
                    problem.visited = {(i, j)}
                    node = dfs(problem)
                    if node:
                        words.add(node.state[1])
    return words


if __name__ == "__main__":
    board = [
        ["К", "О", "Т", "А"],
        ["Р", "А", "К", "Т"],
        ["Л", "И", "С", "Ы"],
        ["М", "Е", "Д", "В"]
    ]
    dictionary = ["КОТ", "ЛИС", "РАК", "МЕДВЕДЬ"]
    words = solve(board, dictionary)
    print(words)

    print("\n")
    board = [
        ["Д", "Е", "Р", "Е", "В"],
        ["О", "С", "Т", "О", "К"],
        ["Г", "О", "Р", "А", "Л"],
        ["С", "Т", "Р", "О", "Й"]
    ]
    dictionary = ["ДЕРЕВО", "СТРОЙ", "ГОРА", "ОСТРОК"]
    words = solve(board, dictionary)
    print(words)
