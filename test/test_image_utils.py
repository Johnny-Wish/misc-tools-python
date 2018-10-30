import image_utils
import numpy as np
from PIL import Image
import unittest


class ImageUtilsTestCase(unittest.TestCase):
    """
    Test case for image_utils.py
    """

    @staticmethod
    def get_random_rgb_image(low=0, high=256, width=640, height=480):
        return Image.fromarray(np.random.randint(low, high, (width, height, 3), dtype=np.uint8), "RGB")

    @staticmethod
    def get_pure_color_image(mode="RGB", color=0, width=640, height=480):
        return Image.new(mode, (width, height), color=color)

    def test_auto_alpha(self):
        img = self.get_random_rgb_image(200, 256)
        new_img = image_utils.auto_alpha(img)

        img.show()
        new_img.show()
        self.assertTupleEqual(img.size, new_img.size)

        arr1 = np.asarray(img)
        arr2 = np.asarray(new_img)[:, :, :3]
        self.assertTupleEqual(arr1.shape, arr2.shape)
        self.assertTrue(np.allclose(arr1, arr2))


if __name__ == '__main__':
    unittest.main()
