from PIL import Image


class GridDisplayer:
    def __init__(self, images, layout, grid_shape=None, margin_shape=None):
        self.images = images
        self.layout = layout
        self._grid_shape = None
        self._margin_shape = None
        self.grid_shape = grid_shape
        self.margin_shape = margin_shape

    @property
    def margin_shape(self):
        return self._margin_shape

    @margin_shape.setter
    def margin_shape(self, value):
        if value is None:
            self._margin_shape = (0, 0)
        elif hasattr(value, "__len__"):
            try:
                self._margin_shape = tuple(value[:2])
            except IndexError as e:
                print(e)
                raise IndexError("Illegal margin shape")
        else:
            self._margin_shape = (value, value)

    @property
    def grid_shape(self):
        return self._grid_shape

    @grid_shape.setter
    def grid_shape(self, value):
        if value is None:
            self._grid_shape = (64, 64)
        elif hasattr(value, "__len__"):
            try:
                self._grid_shape = tuple(value[:2])
            except IndexError as e:
                print(e)
                raise IndexError("Illegal grid shape")
        else:
            self._grid_shape = (value, value)

    def generate(self):
        width = self.layout[0] * (self.grid_shape[0] + self.margin_shape[0]) - self.margin_shape[0]
        heigth = self.layout[1] * (self.grid_shape[1] + self.margin_shape[1]) - self.margin_shape[1]
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
    displayer = GridDisplayer(images, (10, 4))
    grids = displayer.generate()
    grids.save(os.path.join(parent_dir + "0_preview.jpg"))
