from io import UnsupportedOperation
from pilkit.exceptions import UnknownFormat, UnknownExtension
from pilkit.lib import Image
from pilkit.utils import (extension_to_format, format_to_extension, FileWrapper,
                          save_image, prepare_image)
from nose.tools import eq_, raises, ok_
from tempfile import NamedTemporaryFile
from .utils import create_image


def test_extension_to_format():
    eq_(extension_to_format('.jpeg'), 'JPEG')
    eq_(extension_to_format('.rgba'), 'SGI')


def test_format_to_extension_no_init():
    eq_(format_to_extension('PNG'), '.png')
    eq_(format_to_extension('ICO'), '.ico')


@raises(UnknownFormat)
def test_unknown_format():
    format_to_extension('TXT')


@raises(UnknownExtension)
def test_unknown_extension():
    extension_to_format('.txt')


def test_default_extension():
    """
    Ensure default extensions are honored.

    Since PIL's ``Image.EXTENSION`` lists ``'.jpe'`` before the more common
    JPEG extensions, it would normally be the extension we'd get for that
    format. ``pilkit.utils.DEFAULT_EXTENSIONS`` is our way of specifying which
    extensions we'd prefer, and this tests to make sure it's working.

    """
    eq_(format_to_extension('JPEG'), '.jpg')


@raises(AttributeError)
def test_filewrapper():

    class K(object):
        def fileno(self):
            raise UnsupportedOperation

    FileWrapper(K()).fileno()


def test_save_with_filename():
    """
    Test that ``save_image`` accepts filename strings (not just file objects).
    This is a test for GH-8.

    """
    im = create_image()
    outfile = NamedTemporaryFile()
    save_image(im, outfile.name, 'JPEG')
    outfile.close()


def test_format_normalization():
    """
    Make sure formats are normalized by ``prepare_image()``.
    See https://github.com/matthewwithanm/django-imagekit/issues/262
    """
    im = Image.new('RGBA', (100, 100))
    ok_('transparency' in prepare_image(im, 'gIF')[1])
