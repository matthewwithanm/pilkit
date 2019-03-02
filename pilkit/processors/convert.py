
class Convert(object):
    """
    Converts image to different mode
    """

    def __init__(self, mode):
        """
        :param mode: Define the mode to which an image is to be converted

        """
        self.mode = mode

    def process(self, img):
        return img.convert(self.mode)
