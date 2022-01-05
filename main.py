#!/usr/bin/env python3

import itertools
import numpy as np
import typing

class Board:
    possible_moves = {
        (e[1] * e[0], e[2] * (3 - e[0]))
        for e in itertools.product(
            {1, 2},
            {1, -1},
            {1, -1},
        )
    }

    def __init__(
        self,
        no_rows: int=8,
        no_cols: int=8,
        first: tuple[int, int] = None,
    ):
        self.no_rows: int = no_rows
        self.no_cols: int = no_cols

        self.fields: np.ndarray = np.full((no_rows, no_cols), False)

        self.current: tuple[int, int] = None
        if first:
            self.set_knight(first)

        self.no_pad: int = 1
        self.col_sep: str = "|"
        self.row_sep: str = (
            "\n"
            + (2 * no_cols - 1) * "-"
            + 2 * self.no_pad * no_cols * "-"
            + "\n"
        )

    def __repr__(self) -> str:
        return "".join(
            [
                1
                if self[i, j]
                else 0
                for i in range(self.no_rows)
                for j in range(self.no_cols)
            ]
        )

    def __str__(self) -> str:
        res = "\n"

        ls_rows = []
        for i in range(self.no_rows):
            ls_row = [
                self.no_pad * " "
                + ("x" if self[i, j] else " ")
                + self.no_pad * " "
                for j in range(self.no_cols)
            ]
            s_row = self.col_sep.join(ls_row)
            ls_rows.append(s_row)

        res += self.row_sep.join(ls_rows)
        res += "\n"

        return res

    def __getitem__(self, idx: tuple[int, int]) -> bool:
        return self.fields[idx]

    def __setitem__(self, idx: tuple[int, int], val: bool):
        assert isinstance(val, bool)
        self.fields[idx] = val

    def set_knight(self, idx: tuple[int, int]):
        self[idx] = True
        self.current = idx

    def add(self, move: tuple[int, int]) -> tuple[int, int]:
        return (self.current[0] + move[0], self.current[1] + move[1])

    def is_valid(self, move: tuple[int, int]) -> bool:
        next_position = self.add(move)

        if next_position[0] < 0 or next_position[0] >= self.no_rows:
            return False

        if next_position[1] < 0 or next_position[1] >= self.no_cols:
            return False

        return not self[next_position]

    @property
    def valid_moves(self) -> set[tuple[int, int]]:
        return {
            move_it
            for move_it in Board.possible_moves
            if self.is_valid(move_it)
        }

if __name__ == "__main__":
    board = Board(first=(0, 0))
    print(board)
    print(board.valid_moves)

