from pygame import draw
from pygame import Rect


class Field:
    def __init__(self, w, h, cell_size, line_width=1):
        self.w = w
        self.h = h
        self.cell_size = cell_size
        self.line_width = line_width

    def get_grid_placement_by_pos(self, pos):
        column = pos[0] // self.cell_size
        row = pos[1] // self.cell_size

        return (column, row)

    def draw(self, surface, color="black"):
        drawable_rects = self._get_drawable_rects()
        for rect in drawable_rects:
            draw.rect(surface, color, rect, width=1)

    def _get_drawable_rects(self):
        drawable_rects = []

        for i in range(self.w):
            for j in range(self.h):
                pos = (i * self.cell_size, j * self.cell_size)
                drawable_rects.append(
                    Rect(
                        pos,
                        (
                            self.cell_size + self.line_width,
                            self.cell_size + self.line_width,
                        ),
                    )
                )

        return drawable_rects
