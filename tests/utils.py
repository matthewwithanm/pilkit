import os
from pilkit.lib import Image


def get_image_file():
    """
    See also:

    http://en.wikipedia.org/wiki/Lenna
    http://sipi.usc.edu/database/database.php?volume=misc&image=12

    """
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'assets', 'lenna.png')
    return open(path, 'r+b')


def create_image():
    return Image.open(get_image_file())
