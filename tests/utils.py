import os
from pilkit.lib import Image


def get_image_file(image_name='reference.png'):
    """
    See also:

    http://en.wikipedia.org/wiki/Lenna
    http://sipi.usc.edu/database/database.php?volume=misc&image=12

    """
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'assets', image_name)
    return open(path, 'r+b')

def create_image():
    return Image.open(get_image_file())

def compare_images(a, b):
  if a.size != b.size:
    return False

  rows, cols = a.size

  for row in range(rows):
    for col in range(cols):
      if a.getpixel((row, col)) != b.getpixel((row, col)):
        return False

  return True
