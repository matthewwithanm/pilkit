from ..lib import Image, ImageMode


def color_count(image):
    """ Return the number of color values in the input image --
        this is the number of pixels times the band count
        of the image.
    """
    mode_descriptor = ImageMode.getmode(image.mode)
    width, height = image.size
    return width * height * len(mode_descriptor.bands)

def histogram_entropy_py(image):
    """ Calculate the entropy of an images' histogram. """
    from math import log2, fsum
    histosum = float(color_count(image))
    histonorm = (histocol / histosum for histocol in image.histogram())
    return -fsum(p * log2(p) for p in histonorm if p != 0.0)

# Select the Pillow native histogram entropy function - if
# available - and fall back to the Python implementation:
histogram_entropy = getattr(Image.Image, 'entropy', histogram_entropy_py)

def resolve_palette(image):
    """ Convert a palette image to a non-palette image. """

    # We need to load the image before accessing the palette
    image.load()

    if image.palette is None:
        return image
    return image.convert(image.palette.mode)