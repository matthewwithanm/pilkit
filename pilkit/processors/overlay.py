from pilkit.lib import Image


class ColorOverlay(object):
    """
    Overlay a color mask with a the given opacity
    """

    def __init__(self, color, overlay_opacity=0.5):
        """
        :pamra color: `ImageColor` instance to overlay on the original image
        :param overlay_opacity: Define the fusion factor for the overlay mask

        """
        self.color = color
        self.overlay_opacity = overlay_opacity

    def process(self, img):
        original = img = img.convert('RGB')
        overlay = Image.new('RGB', original.size, self.color)
        mask = Image.new('RGBA', original.size, (0,0,0,int((1.0 - self.overlay_opacity)*255)))
        img = Image.composite(original, overlay, mask).convert('RGB')
        return img
