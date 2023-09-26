# flake8: noqa

# Required PIL classes may or may not be available from the root namespace
# depending on the installation method used.
try:
    from PIL import Image, ImageColor, ImageChops, ImageEnhance, ImageFile, \
            ImageFilter, ImageDraw, ImageStat, ImageMode
except ImportError:
    try:
        import Image
        import ImageColor
        import ImageChops
        import ImageEnhance
        import ImageFile
        import ImageFilter
        import ImageDraw
        import ImageStat
        import ImageMode
    except ImportError:
        raise ImportError('PILKit was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.')

try:
    from io import BytesIO as StringIO
except ImportError as exc:
    try:
        from cStringIO import StringIO
    except ImportError:
        try:
            from StringIO import StringIO
        except ImportError:
            raise exc

try:
    string_types = [basestring, str]
except NameError:
    string_types = [str]


def getattrsafe(obj, attr, fallback_attr = None):
    """Similar to getattr but accept dotted path

    The idea of this function is to pass dotted path to attribute.
    If the path is missing then the fallback will be evaluated as dotted path also.
    If the fallback is not present then the attribute error for the first path is thrown

    The main idea of this function is for compatibility with Pillow < 10

    Example::

        >>> from PIL import Image
        >>> getattrsafe(Image, 'Transpose.FLIP_HORIZONTAL', 'FLIP_HORIZONTAL')
    """
    names = attr.split('.')
    res = obj
    for i, name in enumerate(names):
        try:
            res = getattr(res, name)
        except AttributeError:
            missing = '.'.join(names[:i + 1])
            if fallback_attr is None:
                raise AttributeError("'{}' object has no attribute '{}'".format(type(obj).__name__, missing))
            else:
                try:
                    return getattrsafe(obj, fallback_attr)
                except AttributeError:
                    raise AttributeError("'{}' object has no attribute '{}' or '{}'".format(type(obj).__name__, missing, fallback_attr))
    return res
