from typing import Tuple, List


Color = Tuple[int, int, int]


class ScreenPoint:
    x: int = None
    y: int = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x}, {self.y}"


class ScreenBlock:
    """
    position - line (2 points) that conform rectangle
    position: tuple(ScreenPoint, ScreenPoint)
    """
    _position: ScreenPoint = None
    _width: int = None
    _height: int = None
    _color: Color = (None, None, None)

    def __init__(self, position: ScreenPoint = None, width: int = None, height: int = None, color: Color = None):
        self._position = position
        self._width = width
        self._height = height
        self._color = color

    @property
    def color(self):
        return self._color

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def position(self):
        return self._position

    @color.setter
    def color(self, value: Color):
        self._color = value

    @width.setter
    def width(self, value):
        self._width = value

    @height.setter
    def height(self, value):
        self._height = value

    @position.setter
    def position(self, value):
        self._position = value

    def __repr__(self):
        return f"pos - {self.position}, w - {self.width}, h - {self.height}, c - ({self.color})"


class ScreenMesh:
    _mesh: List[List[ScreenBlock]] = []
    vertical_proportion: int = None
    horizontal_proportion: int = None

    def __init__(self, size: Tuple[int, int]):
        for y in range(0, size[1]):
            inline_blocks = []
            for x in range(0, size[0]):
                inline_blocks.append(ScreenBlock())
            self._mesh.append(inline_blocks)

    @property
    def mesh(self):
        return self._mesh

    def set_proportions(self, proportions: tuple):
        h_prop, v_prop = proportions
        self.vertical_proportion = self.normalize_proportion(v_prop)
        self.horizontal_proportion = self.normalize_proportion(h_prop)

    @staticmethod
    def normalize_proportion(value):
        """Drop fraction part of propotrions"""
        return round(value - (value % 1))

    def set_screen_block_color(self, vertical_index: int, horizontal_index: int, color: Color):
        self._mesh[vertical_index][horizontal_index].color = color

    def set_screen_block_position(self, vertical_index: int, horizontal_index: int, position: ScreenPoint):
        self._mesh[vertical_index][horizontal_index].position = position

    def set_screen_block_position_by_coordinate(self, vertical_index: int, horizontal_index: int, x: int, y: int):
        self._mesh[vertical_index][horizontal_index].position = ScreenPoint(x, y)

    def set_screen_block_width(self, vertical_index: int, horizontal_index: int, width: int):
        self._mesh[vertical_index][horizontal_index].width = width

    def set_screen_block_height(self, vertical_index: int, horizontal_index: int, height: int):
        self._mesh[vertical_index][horizontal_index].height = height

    def __iter__(self):
        return self.mesh.__iter__()
