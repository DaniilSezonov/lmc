from PIL import ImageGrab
from config import HORYZONTAL_BLOCKS_COUNT, VERTICAL_BLOCKS_COUNT
from screen import ScreenModel


class ScreenGrabber:
    screen_size = (None, None)
    screen_model = None

    def __init__(self):
        image = ImageGrab.grab()
        self.screen_size = image.size
        self.screen_model = ScreenModel(self.screen_size, (HORYZONTAL_BLOCKS_COUNT, VERTICAL_BLOCKS_COUNT))

    def synchronize(self):
        image = ImageGrab.grab()
        for model_line in self.screen_model.scree_mesh:
            for model_block in model_line:
                cropped_image = image.crop(
                    box=(model_block.position.x,
                         model_block.position.y,
                         model_block.position.x + model_block.width,
                         model_block.position.y + model_block.height
                         )
                )
                avg_color = self.getAverageRGB(cropped_image)
                model_block.color = tuple(round(c) for c in avg_color)

    def getAverageRGB(self, image):
        """
        Given PIL Image, return average value of color as (r, g, b)
        """
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


