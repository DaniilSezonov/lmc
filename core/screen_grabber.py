from time import time

from PIL import Image
from mss import mss

from core.config import HORIZONTAL_BLOCKS_COUNT, VERTICAL_BLOCKS_COUNT
from core.screen import ScreenModel


class ScreenGrabber:
    screen_size = (None, None)
    screen_model = None

    def __init__(self):
        self.monitor = mss().monitors[1]
        image = self.get_screen_image()
        self.screen_size = image.size
        self.screen_model = ScreenModel(self.screen_size, (HORIZONTAL_BLOCKS_COUNT, VERTICAL_BLOCKS_COUNT))

    def synchronize(self):
        image = self.get_screen_image()
        for model_block in self.screen_model.screen_mesh:
            cropped_image = image.crop(
                box=(model_block.position.x,
                     model_block.position.y,
                     model_block.position.x + model_block.width,
                     model_block.position.y + model_block.height
                     )
            )
            avg_color = self.getAverageRGB(cropped_image)
            model_block.color = (round(avg_color[0]), round(avg_color[1]), round(avg_color[2]))

    def get_screen_image(self):
        sct_img = mss().grab(self.monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    def getAverageRGB(self, image):
        # no. of pixels in image
        npixels = image.size[0] * image.size[1]
        # get colors as [(cnt1, (r1, g1, b1)), ...]
        cols = image.getcolors(npixels)
        # get [(c1*r1, c1*g1, c1*g2),...]
        sumRGB = [(x[0] * x[1][0], x[0] * x[1][1], x[0] * x[1][2]) for x in cols]
        # calculate (sum(ci*ri)/np, sum(ci*gi)/np, sum(ci*bi)/np)
        # the zip gives us [(c1*r1, c2*r2, ..), (c1*g1, c1*g2,...)...]
        avg = tuple([sum(x) / npixels for x in zip(*sumRGB)])
        return avg


