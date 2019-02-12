from typing import Tuple, List


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
    position: ScreenPoint = None
    width: int = None
    height: int = None
    color: Tuple[int, int, int] = (None, None, None)

    def __init__(self, position: ScreenPoint, width: int, height: int):
        self.position = position
        self.width = width
        self.height = height

    def __repr__(self):
        return f"pos - {self.position}, w - {self.width}, h - {self.height}, c - ({self.color})"


class ScreenModel:
    """
    resolution - current screen resolution
    model_size - size of mash
    """
    resolution: Tuple[int, int] = (None, None)

    model_size: Tuple[int, int] = (None, None)
    scree_mesh: List[List[ScreenBlock]] = []

    def __init__(self, resolution: Tuple[int, int], model_size: Tuple[int, int]):
        self.resolution = resolution
        self.model_size = model_size
        self.generate_mesh()

    def generate_mesh(self):
        h_proportion = round(self.resolution[0] / self.model_size[0], 1)
        v_proportion = round(self.resolution[1] / self.model_size[1], 1)
        v_proportion = round(v_proportion - (v_proportion % 1))
        h_proportion = round(h_proportion - (h_proportion % 1))
        uncomposed_pixels_count_v = self.resolution[1] - (v_proportion * self.model_size[1])
        uncomposed_pixels_count_h = self.resolution[0] - (h_proportion * self.model_size[0])

        current_v_position = 0
        for v in range(self.model_size[1]):
            has_extra_pixel_h, allocated_height = self.pixel_allocator(v_proportion, v, self.model_size[1], uncomposed_pixels_count_v)
            blocks = []
            current_h_position = 0
            for h in range(self.model_size[0]):
                has_extra_pixel_w, allocated_width = self.pixel_allocator(h_proportion, h, self.model_size[0], uncomposed_pixels_count_h)
                block = ScreenBlock(
                    position=ScreenPoint(x=current_h_position, y=current_v_position),
                    width=allocated_width,
                    height=allocated_height,
                )
                current_h_position += allocated_width
                blocks.append(block)
            current_v_position += allocated_height
            self.scree_mesh.append(blocks)

    def pixel_allocator(self, size, block_number, inline_blocks_count, uncomposed_pixels_count) -> Tuple[bool, int]:
        result = size
        has_extra_pixel = False
        if inline_blocks_count % 2:
            # distributable_blocks - Tuple(middle position, blocks_count)
            distributable_blocks = (round(((inline_blocks_count-1)/2)+((inline_blocks_count/2) % 1)), 1)
        else:
            distributable_blocks = (round((inline_blocks_count-1) / 2), 2)
            if uncomposed_pixels_count % 2:
                has_extra_pixel = True
        if distributable_blocks[0] <= block_number < distributable_blocks[0] + distributable_blocks[1]:
            result += round(uncomposed_pixels_count/distributable_blocks[1])

        return has_extra_pixel, result
