from PIL import ImageFilter

class GaussianBlur(object):
    """
    Performs Gaussian blur filter on image.
    """

    def __init__(self, radius):
        """
        :param radius: Blur radius (passed to GaussianBlur filter)
        """

        self.radius = radius

    def process(self, img):
        return img.filter(ImageFilter.GaussianBlur(self.radius))
