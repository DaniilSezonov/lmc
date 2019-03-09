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
    _color: Color = (None, None, None)
    _position: ScreenPoint = None
    _width: int = None
    _height: int = None

    def __init__(self, position: ScreenPoint = None, width: int = None, height: int = None, color: Color = (None, None, None)):
        self._position = position
        self._width = width
        self._height = height
        self._color = color

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def position(self):
        return self._position

    @width.setter
    def width(self, value):
        self._width = value

    @height.setter
    def height(self, value):
        self._height = value

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value

    def __repr__(self):
        return f"pos - {self.position}, w - {self.width}, h - {self.height}, c - ({self.color})"


class ScreenMesh:
    _full_mesh: List[List[ScreenBlock]] = []
    _usable_mesh: List[ScreenBlock] = []
    _excludable_mesh: List[ScreenBlock] = []
    _current_index = (0, 0)
    vertical_proportion: int = None
    horizontal_proportion: int = None

    def __init__(self, size: Tuple[int, int]):
        for y in range(0, size[1]):
            for x in range(0, size[0]):
                self._usable_mesh.append(ScreenBlock())
            self._full_mesh.append(self._usable_mesh[y*size[0]:(y+1)*size[0]])

    @property
    def mesh(self):
        return self._usable_mesh

    def set_proportions(self, proportions: tuple):
        h_prop, v_prop = proportions
        self.vertical_proportion = self.normalize_proportion(v_prop)
        self.horizontal_proportion = self.normalize_proportion(h_prop)

    @staticmethod
    def normalize_proportion(value):
        """Drop fraction part of proportions"""
        return round(value - (value % 1))

    def set_screen_block_color(self, vertical_index: int, horizontal_index: int, color: Color):
        self._full_mesh[vertical_index][horizontal_index].color = color

    def set_screen_block_position(self, vertical_index: int, horizontal_index: int, position: ScreenPoint):
        self._full_mesh[vertical_index][horizontal_index].position = position

    def set_screen_block_position_by_coordinate(self, vertical_index: int, horizontal_index: int, x: int, y: int):
        self._full_mesh[vertical_index][horizontal_index].position = ScreenPoint(x, y)

    def set_screen_block_width(self, vertical_index: int, horizontal_index: int, width: int):
        self._full_mesh[vertical_index][horizontal_index].width = width

    def set_screen_block_height(self, vertical_index: int, horizontal_index: int, height: int):
        self._full_mesh[vertical_index][horizontal_index].height = height

    def exclude_mesh_part(self, indexes: [Tuple[int, int]]):
        self._usable_mesh.clear()
        self._excludable_mesh.clear()
        for v_index, v_blocks in enumerate(self._full_mesh):
            for h_index, h_block in enumerate(v_blocks):
                for v_exclude_index, h_exclude_index in indexes:
                    if v_exclude_index == v_index and h_exclude_index == h_index:
                        self._excludable_mesh.append(h_block)
                    else:
                        self._usable_mesh.append(h_block)

    def __iter__(self):
        return self._usable_mesh.__iter__()




