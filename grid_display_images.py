from PIL import Image


class GridDisplayer:
    def __init__(self, images, n_cols, n_rows, grid_shape, margin_shape):
        self.images = images
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid_shape = grid_shape
        self.margin_shape = margin_shape

    def generate(self):
        width = self.n_cols * (self.grid_shape[0] + self.margin_shape[0]) - self.margin_shape[0]
        heigth = self.n_rows * (self.grid_shape[1] + self.margin_shape[1]) - self.margin_shape[1]
        image_iterator = iter(self.images)

        image_grids = Image.new("RGB", (width, heigth))

        try:
            for i in range(0, width, self.grid_shape[0] + self.margin_shape[0]):
                for j in range(0, heigth, self.grid_shape[1] + self.margin_shape[1]):
                    # REVIEW might be (j, i)
                    image_grids.paste(next(image_iterator).resize((self.grid_shape[0], self.grid_shape[1])), (i, j))
        except StopIteration:
            pass

        return image_grids


if __name__ == '__main__':
    import glob
    import os
    from itertools import chain

    parent_dir = "/Users/liushuheng/Desktop/citrus-canker-mixed-227x227/"
    path = os.path.join(parent_dir, "0")
    filenames = chain.from_iterable(glob.glob(os.path.join(path, "*" + ext)) for ext in ["jpg", "JPG"])
    images = (Image.open(filename) for filename in filenames)
    displayer = GridDisplayer(images, 5, 3, (227, 227), (2, 2))
    grids = displayer.generate()
    grids.save(os.path.join(parent_dir + "0_preview.jpg"))
