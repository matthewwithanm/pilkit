import os
import mimetypes
import sys
from .exceptions import UnknownExtension, UnknownFormat
from .lib import Image, ImageFile, StringIO


RGBA_TRANSPARENCY_FORMATS = ['PNG']
PALETTE_TRANSPARENCY_FORMATS = ['PNG', 'GIF']
DEFAULT_EXTENSIONS = {
    'JPEG': '.jpg',
}


def img_to_fobj(img, format, autoconvert=True, **options):
    return save_image(img, StringIO(), format, options, autoconvert)


def open_image(target):
    target.seek(0)
    return Image.open(target)


_pil_init = 0


def _preinit_pil():
    """Loads the standard PIL file format drivers. Returns True if ``preinit()``
    was called (and there's a potential that more drivers were loaded) or False
    if there is no possibility that new drivers were loaded.

    """
    global _pil_init
    if _pil_init < 1:
        Image.preinit()
        _pil_init = 1
        return True
    return False


def _init_pil():
    """Loads all PIL file format drivers. Returns True if ``init()`` was called
    (and there's a potential that more drivers were loaded) or False if there is
    no possibility that new drivers were loaded.

    """
    global _pil_init
    _preinit_pil()
    if _pil_init < 2:
        Image.init()
        _pil_init = 2
        return True
    return False


def _extension_to_format(extension):
    return Image.EXTENSION.get(extension.lower())


def _format_to_extension(format):
    if format:
        format = format.upper()
        if format in DEFAULT_EXTENSIONS:
            ext = DEFAULT_EXTENSIONS[format]

            # It's not enough for an extension to be listed in
            # ``DEFAULT_EXTENSIONS``, it must also be recognized by PIL.
            if ext in Image.EXTENSION:
                return ext
        for k, v in Image.EXTENSION.items():
            if v == format:
                return k
    return None


def extension_to_mimetype(ext):
    try:
        filename = 'a%s' % (ext or '')  # guess_type requires a full filename, not just an extension
        mimetype = mimetypes.guess_type(filename)[0]
    except IndexError:
        mimetype = None
    return mimetype


def format_to_mimetype(format):
    return extension_to_mimetype(format_to_extension(format))


def extension_to_format(extension):
    """Returns the format that corresponds to the provided extension.

    """
    format = _extension_to_format(extension)
    if not format and _preinit_pil():
        format = _extension_to_format(extension)
    if not format and _init_pil():
        format = _extension_to_format(extension)
    if not format:
        raise UnknownExtension(extension)
    return format


def format_to_extension(format):
    """Returns the first extension that matches the provided format.

    """
    extension = None
    if format:
        extension = _format_to_extension(format)
        if not extension and _preinit_pil():
            extension = _format_to_extension(format)
        if not extension and _init_pil():
            extension = _format_to_extension(format)
    if not extension:
        raise UnknownFormat(format)
    return extension


def suggest_extension(name, format):
    original_extension = os.path.splitext(name)[1]
    try:
        suggested_extension = format_to_extension(format)
    except UnknownFormat:
        extension = original_extension
    else:
        if suggested_extension.lower() == original_extension.lower():
            extension = original_extension
        else:
            try:
                original_format = extension_to_format(original_extension)
            except UnknownExtension:
                extension = suggested_extension
            else:
                # If the formats match, give precedence to the original extension.
                if format.lower() == original_format.lower():
                    extension = original_extension
                else:
                    extension = suggested_extension
    return extension


def save_image(img, outfile, format, options=None, autoconvert=True):
    """
    Wraps PIL's ``Image.save()`` method. There are two main benefits of using
    this function over PIL's:

    1. It gracefully handles the infamous "Suspension not allowed here" errors.
    2. It prepares the image for saving using ``prepare_image()``, which will do
        some common-sense processing given the target format.

    """
    options = options or {}

    if autoconvert:
        img, save_kwargs = prepare_image(img, format)
        # Use returned from prepare_image arguments for base
        # and update them with provided options. Then use the result
        save_kwargs.update(options)
        options = save_kwargs

    # Attempt to reset the file pointer.
    try:
        outfile.seek(0)
    except AttributeError:
        pass

    try:
        with quiet():
            img.save(outfile, format, **options)
    except IOError:
        # PIL can have problems saving large JPEGs if MAXBLOCK isn't big enough,
        # So if we have a problem saving, we temporarily increase it. See
        # http://github.com/jdriscoll/django-imagekit/issues/50 and
        # https://github.com/jdriscoll/django-imagekit/issues/134
        old_maxblock = ImageFile.MAXBLOCK
        ImageFile.MAXBLOCK = sys.maxint
        try:
            img.save(outfile, format, **options)
        finally:
            ImageFile.MAXBLOCK = old_maxblock

    try:
        outfile.seek(0)
    except AttributeError:
        pass

    return outfile


class quiet(object):
    """
    A context manager for suppressing the stderr activity of PIL's C libraries.
    Based on http://stackoverflow.com/a/978264/155370

    """
    def __enter__(self):
        self.stderr_fd = sys.__stderr__.fileno()
        self.null_fd = os.open(os.devnull, os.O_RDWR)
        self.old = os.dup(self.stderr_fd)
        os.dup2(self.null_fd, self.stderr_fd)

    def __exit__(self, *args, **kwargs):
        os.dup2(self.old, self.stderr_fd)
        os.close(self.null_fd)
        os.close(self.old)


def prepare_image(img, format):
    """
    Prepares the image for saving to the provided format by doing some
    common-sense conversions. This includes things like preserving transparency
    and quantizing. This function is used automatically by ``save_image()``
    immediately before saving unless you specify ``autoconvert=False``. It is
    provided as a utility for those doing their own processing.

    :param img: The image to prepare for saving.
    :param format: The format that the image will be saved to.

    """
    make_opaque = False
    save_kwargs = {}

    if img.mode == 'RGBA':
        if format in RGBA_TRANSPARENCY_FORMATS:
            pass
        elif format in PALETTE_TRANSPARENCY_FORMATS:
            # If you're going from a format with alpha transparency to one
            # with palette transparency, transparency values will be
            # snapped: pixels that are more opaque than not will become
            # fully opaque; pixels that are more transparent than not will
            # become fully transparent. This will not produce a good-looking
            # result if your image contains varying levels of opacity; in
            # that case, you'll probably want to use a processor to composite
            # the image on a solid color. The reason we don't do this by
            # default is because not doing so allows processors to treat
            # RGBA-format images as a super-type of P-format images: if you
            # have an RGBA-format image with only a single transparent
            # color, and save it as a GIF, it will retain its transparency.
            # In other words, a P-format image converted to an
            # RGBA-formatted image by a processor and then saved as a
            # P-format image will give the expected results.

            # Work around a bug in PIL: split() doesn't check to see if
            # img is loaded.
            img.load()

            alpha = img.split()[-1]
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE,
                    colors=255)
            img.paste(255, mask)
            save_kwargs['transparency'] = 255
        else:
            # Simply converting an RGBA-format image to an RGB one creates a
            # gross result, so we paste the image onto a white background. If
            # that's not what you want, that's fine: use a processor to deal
            # with the transparency however you want. This is simply a
            # sensible default that will always produce something that looks
            # good. Or at least, it will look better than just a straight
            # conversion.
            make_opaque = True
    elif img.mode == 'P':
        if format in PALETTE_TRANSPARENCY_FORMATS:
            try:
                save_kwargs['transparency'] = img.info['transparency']
            except KeyError:
                pass
        elif format in RGBA_TRANSPARENCY_FORMATS:
            # Currently PIL doesn't support any RGBA-mode formats that
            # aren't also P-mode formats, so this will never happen.
            img = img.convert('RGBA')
        else:
            make_opaque = True
    else:
        img = img.convert('RGB')

        # GIFs are always going to be in palette mode, so we can do a little
        # optimization. Note that the RGBA sources also use adaptive
        # quantization (above). Images that are already in P mode don't need
        # any quantization because their colors are already limited.
        if format == 'GIF':
            img = img.convert('P', palette=Image.ADAPTIVE)

    if make_opaque:
        from .processors import MakeOpaque
        img = MakeOpaque().process(img).convert('RGB')

    if format == 'JPEG':
        save_kwargs['optimize'] = True

    return img, save_kwargs


def process_image(img, processors=None, format=None, autoconvert=True, options=None):
    from .processors import ProcessorPipeline

    original_format = img.format

    # Run the processors
    img = ProcessorPipeline(processors or []).process(img)

    format = format or img.format or original_format or 'JPEG'
    options = options or {}
    return img_to_fobj(img, format, autoconvert, **options)
