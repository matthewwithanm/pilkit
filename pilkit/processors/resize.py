from .base import Anchor
from ..lib import Image


class Resize(object):
    """
    Resizes an image to the specified width and height.

    """
    def __init__(self, width, height, upscale=True):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.
        :param upscale: Should the image be enlarged if smaller than the dimensions?

        """
        self.width = width
        self.height = height
        self.upscale = upscale

    def process(self, img):
        if self.upscale or (self.width < img.size[0] and self.height < img.size[1]):
            img = img.convert('RGBA')
            img = img.resize((self.width, self.height), Image.ANTIALIAS)
        return img


class ResizeToCover(object):
    """
    Resizes the image to the smallest possible size that will entirely cover the
    provided dimensions. You probably won't be using this processor directly,
    but it's used internally by ``ResizeToFill`` and ``SmartResize``.

    """
    def __init__(self, width, height, upscale=True):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.

        """
        self.width, self.height = width, height
        self.upscale = upscale

    def process(self, img):
        original_width, original_height = img.size
        ratio = max(float(self.width) / original_width,
                float(self.height) / original_height)
        new_width, new_height = (int(round(original_width * ratio)),
                int(round(original_height * ratio)))
        img = Resize(new_width, new_height, upscale=self.upscale).process(img)
        return img


class ResizeToFill(object):
    """
    Resizes an image, cropping it to the exact specified width and height.

    """

    def __init__(self, width=None, height=None, anchor=None, upscale=True):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.
        :param anchor: Specifies which part of the image should be retained
            when cropping.
        :param upscale: Should the image be enlarged if smaller than the dimensions?

        """
        self.width = width
        self.height = height
        self.anchor = anchor
        self.upscale = upscale

    def process(self, img):
        from .crop import Crop
        img = ResizeToCover(self.width, self.height,
                            upscale=self.upscale).process(img)
        return Crop(self.width, self.height,
                    anchor=self.anchor).process(img)


class SmartResize(object):
    """
    The ``SmartResize`` processor is identical to ``ResizeToFill``, except that
    it uses entropy to crop the image instead of a user-specified anchor point.
    Internally, it simply runs the ``ResizeToCover`` and ``SmartCrop``
    processors in series.
    """
    def __init__(self, width, height, upscale=True):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.
        :param upscale: Should the image be enlarged if smaller than the dimensions?

        """
        self.width, self.height = width, height
        self.upscale = upscale

    def process(self, img):
        from .crop import SmartCrop
        img = ResizeToCover(self.width, self.height,
                            upscale=self.upscale).process(img)
        return SmartCrop(self.width, self.height).process(img)


class ResizeCanvas(object):
    """
    Resizes the canvas, using the provided background color if the new size is
    larger than the current image.

    """
    def __init__(self, width, height, color=None, anchor=None, x=None, y=None):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.
        :param color: The background color to use for padding.
        :param anchor: Specifies the position of the original image on the new
            canvas. Valid values are:

            - Anchor.TOP_LEFT
            - Anchor.TOP
            - Anchor.TOP_RIGHT
            - Anchor.LEFT
            - Anchor.CENTER
            - Anchor.RIGHT
            - Anchor.BOTTOM_LEFT
            - Anchor.BOTTOM
            - Anchor.BOTTOM_RIGHT

            You may also pass a tuple that indicates the position in
            percentages. For example, ``(0, 0)`` corresponds to "top left",
            ``(0.5, 0.5)`` to "center" and ``(1, 1)`` to "bottom right". This is
            basically the same as using percentages in CSS background positions.

        """
        if x is not None or y is not None:
            if anchor:
                raise Exception('You may provide either an anchor or x and y'
                        ' coordinate, but not both.')
            else:
                self.x, self.y = x or 0, y or 0
                self.anchor = None
        else:
            self.anchor = anchor or Anchor.CENTER
            self.x = self.y = None

        self.width = width
        self.height = height
        self.color = color or (255, 255, 255, 0)

    def process(self, img):
        original_width, original_height = img.size

        if self.anchor:
            anchor = Anchor.get_tuple(self.anchor)
            trim_x, trim_y = self.width - original_width, \
                    self.height - original_height
            x = int(float(trim_x) * float(anchor[0]))
            y = int(float(trim_y) * float(anchor[1]))
        else:
            x, y = self.x, self.y

        new_img = Image.new('RGBA', (self.width, self.height), self.color)
        new_img.paste(img, (x, y))
        return new_img


class AddBorder(object):
    """
    Add a border of specific color and size to an image.

    """
    def __init__(self, thickness, color=None):
        """
        :param color: Color to use for the border
        :param thickness: Thickness of the border. Can be either an int or
            a 4-tuple of ints of the form (top, right, bottom, left).
        """
        self.color = color
        if isinstance(thickness, int):
            self.top = self.right = self.bottom = self.left = thickness
        else:
            self.top, self.right, self.bottom, self.left = thickness

    def process(self, img):
        new_width = img.size[0] + self.left + self.right
        new_height = img.size[1] + self.top + self.bottom
        return ResizeCanvas(new_width, new_height, color=self.color,
                x=self.left, y=self.top).process(img)


class ResizeToFit(object):
    """
    Resizes an image to fit within the specified dimensions.

    """

    def __init__(self, width=None, height=None, upscale=True, mat_color=None, anchor=Anchor.CENTER):
        """
        :param width: The maximum width of the desired image.
        :param height: The maximum height of the desired image.
        :param upscale: A boolean value specifying whether the image should
            be enlarged if its dimensions are smaller than the target
            dimensions.
        :param mat_color: If set, the target image size will be enforced and the
            specified color will be used as a background color to pad the image.

        """
        self.width = width
        self.height = height
        self.upscale = upscale
        self.mat_color = mat_color
        self.anchor = anchor

    def process(self, img):
        cur_width, cur_height = img.size
        if not self.width is None and not self.height is None:
            ratio = min(float(self.width) / cur_width,
                    float(self.height) / cur_height)
        else:
            if self.width is None:
                ratio = float(self.height) / cur_height
            else:
                ratio = float(self.width) / cur_width
        new_dimensions = (int(round(cur_width * ratio)),
                          int(round(cur_height * ratio)))
        img = Resize(new_dimensions[0], new_dimensions[1], upscale=self.upscale).process(img)
        if self.mat_color is not None:
            img = ResizeCanvas(self.width, self.height, self.mat_color, anchor=self.anchor).process(img)
        return img


class Thumbnail(object):
    """
    Resize the image for use as a thumbnail. Wraps ``ResizeToFill``,
    ``ResizeToFit``, and ``SmartResize``.

    :param proportion: If set, the processor will pick which of the height or width
        to resize.

    Note: while it doesn't currently, in the future this processor may also
    sharpen based on the amount of reduction.

    """

    def __init__(self, width=None, height=None, anchor=None, crop=None, upscale=None, proportion=None):
        self.width = width
        self.height = height
        self.upscale = upscale
        self.proportion = proportion
        if anchor:
            if crop is False:
                raise Exception("You can't specify an anchor point if crop is False.")
            else:
                crop = True
        elif crop is None:
            # Assume we are cropping if both a width and height are provided. If
            # only one is, we must be resizing to fit.
            crop = width is not None and height is not None

            # A default anchor if cropping.
            if crop and anchor is None:
                anchor = 'auto'
        self.crop = crop
        self.anchor = anchor

    def process(self, img):
        if self.crop:
            if not self.width or not self.height:
                raise Exception('You must provide both a width and height when'
                    ' cropping.')
            if self.anchor == 'auto':
                processor = SmartResize(width=self.width, height=self.height, upscale=self.upscale)
            else:
                processor = ResizeToFill(width=self.width, height=self.height, anchor=self.anchor, upscale=self.upscale)
        else:
            if self.proportion:
                w, h = img.size
                if w > h:
                    self.width = self.proportion
                    self.height = None
                elif w < h:
                    self.height = self.proportion
                    self.width = None
                else:
                    self.height = self.proportion
                    self.width = self.proportion
            processor = ResizeToFit(width=self.width, height=self.height, upscale=self.upscale)
        return processor.process(img)
