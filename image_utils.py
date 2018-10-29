from PIL import Image
from math import ceil, sqrt


class GridCanvasPainter:
    def __init__(self, images, layout=None, grid_shape=None, gap_shape=None, force_list=False, bg_color=None):
        """
        painter for a new canvas with images placed on it as grids
        :param images: iterable, sequence of PIL images
        :param layout: None, int, or tuple, columns by rows of thumbnails to display on canvas,
            if None, automatically uses ceil(sqrt(n_images)) as n_cols, and floor(sqrt(n_images)) as n_rows
            if int, uses `layout` as both n_cols and n_rows
            if tuple, the first integer is construed (n_cols, n_rows),
                if either element in tuple is None, automatically computes the n_cols or n_rows
            note that automatic computation result in listing `images` sequence in MEMORY, which can be inefficient
        :param grid_shape: None, int, or tuple, number of pixels in width and height of each thumbnail
            if None: uses default = 32 * 32
            if int: construed as both width and height for thumbnails
            if tuple: construed as (width, height) for thumbnails
        :param gap_shape: None, int, or tuple, shape of gaps in between thumbnails
            if None: no gap is used, thumbnails are placed right next to each other
            if int: construed as both width and height for gaps
            if tuple: construed as (width, height) for gaps
        :param force_list: bool, if set to True, `images` will be converted to list, default=False
        :param bg_color: int, background color for new canvas, default=None
        """
        if force_list:
            self.images = list(images)
        elif layout is None:
            self.images = list(images)
        elif hasattr(layout, "__contains__") and None in layout:
            self.images = list(images)
        else:
            self.images = images

        # call setters
        self.layout = layout
        self.grid_shape = grid_shape
        self.margin_shape = gap_shape

        if bg_color is None:
            self.bg_color = 0
        else:
            self.bg_color = bg_color

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

        self._canvas = Image.new("RGB", (width, heigth), color=self.bg_color)

        try:
            for j in range(0, heigth, self.grid_shape[1] + self.margin_shape[1]):
                for i in range(0, width, self.grid_shape[0] + self.margin_shape[0]):
                    self._canvas.paste(next(image_iterator).resize((self.grid_shape[0], self.grid_shape[1])), (i, j))
        except StopIteration:
            pass

    # TODO consider force updating
    @property
    def canvas(self):
        if not hasattr(self, "_canvas"):
            self.update_canvas()
        return self._canvas


def paint_grid_canvas(images, layout=None, grid_shape=None, gap_shape=None, force_list=None, bg_color=None):
    """

    :param images: iterable, sequence of PIL images
    :param layout: None, int, or tuple, columns by rows of thumbnails to display on canvas,
        if None, automatically uses ceil(sqrt(n_images)) as n_cols, and floor(sqrt(n_images)) as n_rows
        if int, uses `layout` as both n_cols and n_rows
        if tuple, the first integer is construed (n_cols, n_rows),
            if either element in tuple is None, automatically computes the n_cols or n_rows
        note that automatic computation result in listing `images` sequence in MEMORY, which can be inefficient
    :param grid_shape: None, int, or tuple, number of pixels in width and height of each thumbnail
        if None: uses default = 32 * 32
        if int: construed as both width and height for thumbnails
        if tuple: construed as (width, height) for thumbnails
    :param gap_shape: None, int, or tuple, shape of gaps in between thumbnails
        if None: no gap is used, thumbnails are placed right next to each other
        if int: construed as both width and height for gaps
        if tuple: construed as (width, height) for gaps
    :param force_list: bool, if set to True, `images` will be converted to list, default=False
    :param bg_color: int, background color for new canvas, default=None
    :return: a new canvas with images placed on it as grids
    """

    return GridCanvasPainter(
        images,
        layout=layout,
        grid_shape=grid_shape,
        gap_shape=gap_shape,
        force_list=force_list,
        bg_color=bg_color
    ).canvas


def auto_alpha(image: Image.Image, alpha_value=0, threshold=230):
    assert "RGB" in image.mode, "image has mode {} instead of RGB or RGBA".format(image.mode)

    # No action to perform for an image that already has an alpha channel
    if image.mode == "RGBA":
        return image
    new_image = image.convert("RGBA")

    transform = lambda color: color[:3] + (alpha_value,)
    data = [transform(color) if min(color) > threshold else color for color in new_image.getdata()]
    new_image.putdata(data)
    return new_image


if __name__ == '__main__':
    import glob
    import os
    from itertools import chain

    parent_dir = "/Users/liushuheng/Desktop/citrus-canker-mixed-227x227/"
    path = os.path.join(parent_dir, "1")
    filenames = chain.from_iterable(glob.glob(os.path.join(path, "*" + ext)) for ext in ["jpg", "JPG"])
    images = (Image.open(filename) for filename in filenames)
    paint_grid_canvas(images).save(os.path.join(parent_dir + "1_preview.jpg"))
