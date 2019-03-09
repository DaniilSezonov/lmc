from time import time
from unittest import TestCase

from core.screen_grabber import ScreenGrabber


class ScreenGrabberTests(TestCase):
    def test_synchronize_time(self):
        minimal_time = 0.04
        grabber = ScreenGrabber()
        start_time = time()
        grabber.synchronize()
        print("Время выполнения: ", time() - start_time)
        self.assertTrue(time() - start_time <= minimal_time)