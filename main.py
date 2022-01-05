#!/usr/bin/env python3

import numpy as np

class Board:
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
            self.set(first)

        self.no_pad: int = 1
        self.col_sep: str = "|"
        self.row_sep: str = (
            "\n"
            + (2 * no_cols - 1) * "-"
            + 2 * self.no_pad * no_cols * "-"
            + "\n"
        )

    def __getitem__(self, idx: tuple[int, int]) -> bool:
        return self.fields[idx]

    def __setitem__(self, idx: tuple[int, int], val: bool):
        assert isinstance(val, bool)
        self.fields[idx] = val

    def get(self, idx: tuple[int, int]) -> bool:
        return self[idx]

    def set(self, idx: tuple[int, int]):
        self[idx] = True
        self.current = idx

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

if __name__ == "__main__":
    board = Board()
    print(board)

