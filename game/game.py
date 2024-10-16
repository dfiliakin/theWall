from field.field import Field
import logging
import pygame
from utils.utils import groups


class Game:
    def __init__(self, field: Field):
        self.is_first_player_turn = True
        self.field = field
        self.matrix = [[0 for _ in range(self.field.w)] for _ in range(self.field.h)]
        self.is_going = True

        self.player_sprites = {
            1: pygame.image.load("assets/sprites/x.png"),
            2: pygame.image.load("assets/sprites/o.png"),
        }

    def move(self, pos) -> tuple[int, int, int]:
        x, y = self.field.get_grid_placement_by_pos(pos)
        x, y = self._apply_gravity_to_grid_coords(x, y)

        # Invalid
        if not self._is_valid_coord(x, y):
            logging.warning(f"Invalid coords: {x, y}!")
            return None, None, None

        if self.matrix[y][x]:
            logging.warning(f"This grid cell is not empty: {x, y}")
            return None, None, None

        self.matrix[y][x] = 1 if self.is_first_player_turn else 2
        self.is_first_player_turn = not self.is_first_player_turn
        return self.matrix[y][x], x, y

    def _is_valid_coord(self, x, y):
        if 0 <= x < self.field.w and 0 <= y < self.field.h:
            return True

        return False

    def grid_to_pos(self, x, y):
        return (
            x * self.field.cell_size + self.field.line_width,
            y * self.field.cell_size + self.field.line_width,
        )

    def check_win_condition_around(self, x, y):
        winnable_seqs = []

        logging.debug(f"check_win_condition_around: {(x, y)}")

        # Win by Column
        column = [row[x] for row in self.matrix]
        logging.debug(f" - column: {column}")
        winnable_seqs.append(column)

        # Win by Row
        row = self.matrix[y]
        logging.debug(f" - row: {row}")
        winnable_seqs.append(row)

        # Win by Diagonal (front: / and back: \)
        front_diag = groups(self.matrix, lambda x, y: x + y)[x + y]
        logging.debug(f" - fdiag: {front_diag}")
        winnable_seqs.append(front_diag)

        back_diag = groups(self.matrix, lambda x, y: x - y)[
            max(self.field.h, self.field.w) - 1 - y + x
        ]
        logging.debug(f" - bdiag: {back_diag}")
        winnable_seqs.append(back_diag)

        for seq in winnable_seqs:
            winner = self._check_seq_for_winner(seq)
            if winner:
                self.is_going = False
                return winner

    def _check_seq_for_winner(self, seq):
        stringified = "".join(map(str, seq))
        if "1111" in stringified:
            return 1

        if "2222" in stringified:
            return 2

        return None

    def _apply_gravity_to_grid_coords(self, x, y):

        logging.debug(f"Y before gravity: {y}")

        column = [row[x] for row in self.matrix]
        occupied_cells_number = len(column) - column.count(0)
        y = self.field.h - 1 - occupied_cells_number

        logging.debug(f"Y after gravity: {y}")
        return x, y
