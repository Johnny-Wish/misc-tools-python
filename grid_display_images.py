from PIL import Image
from math import ceil, sqrt


class GridDisplayer:
    def __init__(self, images, layout=None, grid_shape=None, margin_shape=None, force_list=False):
        if force_list:
            self.images = list(images)
        elif layout is None:
            self.images = list(images)
        elif hasattr(layout, "__contains__") and None in layout:
            self.images = list(images)
        else:
            self.images = images

        # initialize attributes
        self._layout = None
        self._grid_shape = None
        self._margin_shape = None

        # call setters
        self.layout = layout
        self.grid_shape = grid_shape
        self.margin_shape = margin_shape

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value):
        if value is None:
            n_cols = ceil(sqrt(len(self.images)))
            n_rows = ceil(len(self.images) / n_cols)
            self._layout = (n_cols, n_rows)
        elif hasattr(value, "__len__"):
            try:
                n_cols = value[0]
                n_rows = value[1]
            except IndexError as e:
                print(e)
                raise IndexError("Illegal layout shape")
            if n_cols is None and n_rows is None:
                # raise ValueError("n_cols and n_rows cannot both be None. Check layout, got {}".format(value))
                self.layout = None
                return
            if n_cols is None:
                n_cols = ceil(len(self.images) / n_rows)
            if n_rows is None:
                n_rows = ceil(len(self.images) / n_cols)
            self._layout = (n_cols, n_rows)
        else:
            self._layout = (value, value)

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

    def update_canvas(self):
        width = self.layout[0] * (self.grid_shape[0] + self.margin_shape[0]) - self.margin_shape[0]
        heigth = self.layout[1] * (self.grid_shape[1] + self.margin_shape[1]) - self.margin_shape[1]
        image_iterator = iter(self.images)

        self._canvas = Image.new("RGB", (width, heigth))

        try:
            for j in range(0, heigth, self.grid_shape[1] + self.margin_shape[1]):
                for i in range(0, width, self.grid_shape[0] + self.margin_shape[0]):
                    self._canvas.paste(next(image_iterator).resize((self.grid_shape[0], self.grid_shape[1])), (i, j))
        except StopIteration:
            pass

    @property
    def canvas(self):
        if not hasattr(self, "_canvas"):
            self.update_canvas()
        return self._canvas


def grid_display(images, layout=None, grid_shape=None, margin_shape=None, force_list=None):
    return GridDisplayer(
        images, layout=layout, grid_shape=grid_shape, margin_shape=margin_shape, force_list=force_list).canvas


if __name__ == '__main__':
    import glob
    import os
    from itertools import chain

    parent_dir = "/Users/liushuheng/Desktop/citrus-canker-mixed-227x227/"
    path = os.path.join(parent_dir, "1")
    filenames = chain.from_iterable(glob.glob(os.path.join(path, "*" + ext)) for ext in ["jpg", "JPG"])
    images = (Image.open(filename) for filename in filenames)
    grid_display(images).save(os.path.join(parent_dir + "1_preview.jpg"))
