from typing import Tuple, List

from core.screen_mesh import ScreenMesh


class ScreenModel:
    """
    resolution - current screen resolution
    model_size - size of mash
    """
    resolution: Tuple[int, int] = (None, None)

    model_size: Tuple[int, int] = (None, None)
    _screen_mesh: ScreenMesh

    def __init__(self, resolution: Tuple[int, int], model_size: Tuple[int, int]):
        self.resolution = resolution
        self.model_size = model_size
        self.screen_mesh = ScreenMesh(self.model_size)
        self.generate_mesh()

    def generate_mesh(self):
        self.screen_mesh.set_proportions(
            (
                round(self.resolution[0] / self.model_size[0], 1),
                round(self.resolution[1] / self.model_size[1], 1)
            )
        )
        uncomposed_pixels_count_v = self.resolution[1] - (self.screen_mesh.vertical_proportion * self.model_size[1])
        uncomposed_pixels_count_h = self.resolution[0] - (self.screen_mesh.horizontal_proportion * self.model_size[0])

        current_v_position = 0
        for v in range(self.model_size[1]):
            has_extra_pixel_h, allocated_height = self.pixel_allocator(
                self.screen_mesh.vertical_proportion,
                v,
                self.model_size[1],
                uncomposed_pixels_count_v
            )
            current_h_position = 0
            for h in range(self.model_size[0]):
                has_extra_pixel_w, allocated_width = self.pixel_allocator(
                    self.screen_mesh.horizontal_proportion,
                    h,
                    self.model_size[0],
                    uncomposed_pixels_count_h
                )

                self.screen_mesh.set_screen_block_position_by_coordinate(v, h, current_v_position, current_h_position)
                self.screen_mesh.set_screen_block_width(v, h, allocated_width)
                self.screen_mesh.set_screen_block_height(v, h, allocated_height)

                current_h_position += allocated_width
            current_v_position += allocated_height

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

    @property
    def screen_mesh(self):
        return self._screen_mesh

    @screen_mesh.setter
    def screen_mesh(self, value):
        self._screen_mesh = value

    def exclude_mesh_part(self, mesh_part):
        pass
