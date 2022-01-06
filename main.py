#!/usr/bin/env python3

import collections
import itertools
import numpy as np
import random
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

    def position_map(
        zero: str,
        one: str,
        two: str,
    ) -> typing.Callable:
        def func(self, i: int, j: int):
            if self[i, j]:
                if self.current == (i, j):
                    return two
                else:
                    return one
            else:
                return zero

        return func

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


    repr_map = position_map("0", "1", "2")

    def __repr__(self) -> str:
        return "".join(
            [
                self.repr_map(i, j)
                for i in range(self.no_rows)
                for j in range(self.no_cols)
            ]
        )

    str_map = position_map(" ", "o", "x")

    def __str__(self) -> str:
        res = "\n"

        ls_rows = []
        for i in range(self.no_rows):
            ls_row = [
                self.no_pad * " "
                + self.str_map(i, j)
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
        assert not self[idx]
        self[idx] = True
        self.current = idx

    def add(self, move: tuple[int, int]) -> tuple[int, int]:
        return (self.current[0] + move[0], self.current[1] + move[1])

    def move(self, move: tuple[int, int]) -> tuple[int, int]:
        assert self.is_valid(move)
        next_position = self.add(move)
        self.set_knight(next_position)

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

    @property
    def is_finished(self) -> bool:
        return len(self.valid_moves) == 0

    @property
    def is_successful(self) -> bool:
        return np.sum(self.fields == 0) == 0

    def copy(self) -> "Board":
        board = Board(self.no_rows, self.no_cols)

        board.fields[:, :] = self.fields
        board.current = self.current

        return board

    def reset(self):
        self.fields[:, :] = False
        self.current = None

class ValueTable:
    def __init__(self):
        self.values: dict[str, float] = collections.defaultdict(lambda: 0.5)

    def __getitem__(self, board: Board) -> float:
        return self.values[repr(board)]

    def __setitem__(self, board: Board, val: float):
        self.values[repr(board)] = val

    def get(
        self,
        board: Board,
        move: tuple[int, int],
    ) -> float:
        board = board.copy()
        board.move(move)
        return self[board]

class Player:
    def __init__(self, board: Board, alpha: float=0.1):
        self.alpha: float = alpha
        self.board: Board = board
        self.table: ValueTable = ValueTable()

    def reset(self):
        self.board.reset()
        self.board.set_knight((0, 0))

    def valid_moves(self) -> list[tuple[int, int]]:
        return sorted(
            self.board.valid_moves,
            key = lambda move: 1.1 * move[0] + move[1],
        )

    def best_move(self, moves) -> tuple[int, int]:
        return max(
            moves,
            key = lambda move: self.table.get(
                self.board,
                move,
            ),
        )

    def pick_move(self, moves):
        weights = [
            self.table.get(
                self.board,
                move,
            )
            for move in moves
        ]

        if all(weight_it == 0.0 for weight_it in weights):
            return self.best_move(moves)

        return random.choices(moves, weights)[0]

    def play(self):
        valid_moves = self.valid_moves()
        best_move = self.best_move(valid_moves)
        move = self.pick_move(valid_moves)

        board = self.board.copy()
        self.board.move(move)
        next_board = self.board.copy()

        if self.board.is_finished:
            if self.board.is_successful:
                self.table[self.board] = 1.0
            else:
                self.table[self.board] = 0.0

        if self.table.get(board, move) == self.table.get(board, best_move):
            self.table[board] += self.alpha * (
                self.table[next_board] - self.table[board]
            )

    def simulate(self, verbose: bool=False):
        self.reset()
        if verbose:
            print(self.board)

        while not self.board.is_finished:
            self.play()
            if verbose:
                print(self.board)

if __name__ == "__main__":
    board = Board(6, 6, first=(0, 0))
    print(board)
    print(board.valid_moves)

    board.move(next(iter(board.valid_moves)))
    print(board)

    player = Player(board)
    player.simulate()
    print(player.table.values)

    import dill

    for i in range(int(1e10)):
        player.simulate()

        if player.board.is_successful:
            print(i, len(player.table.values), len(set(player.table.values.values())))
            print({
                board: value
                for board, value in player.table.values.items()
                if value > 0.5
            })

            with open(f"{i}.pickle", "wb") as f:
                dill.dump(player.table.values, f)

