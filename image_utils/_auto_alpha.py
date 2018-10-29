from PIL import Image


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
