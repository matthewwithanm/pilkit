import os
import io
import pytest
from unittest.mock import Mock, patch
from tempfile import NamedTemporaryFile

from pilkit.exceptions import UnknownFormat, UnknownExtension
from pilkit.lib import Image
from pilkit.utils import (extension_to_format, format_to_extension, FileWrapper,
                          save_image, prepare_image, quiet)

from .utils import create_image


def test_extension_to_format():
    assert extension_to_format('.jpeg') == 'JPEG'
    assert extension_to_format('.rgba') == 'SGI'


def test_format_to_extension_no_init():
    assert format_to_extension('PNG') == '.png'
    assert format_to_extension('ICO') == '.ico'


def test_unknown_format():
    with pytest.raises(UnknownFormat):
        format_to_extension('TXT')


def test_unknown_extension():
    with pytest.raises(UnknownExtension):
        extension_to_format('.txt')


def test_default_extension():
    """
    Ensure default extensions are honored.

    Since PIL's ``Image.EXTENSION`` lists ``'.jpe'`` before the more common
    JPEG extensions, it would normally be the extension we'd get for that
    format. ``pilkit.utils.DEFAULT_EXTENSIONS`` is our way of specifying which
    extensions we'd prefer, and this tests to make sure it's working.

    """
    assert format_to_extension('JPEG') == '.jpg'


def test_filewrapper():

    class K(object):
        def fileno(self):
            raise io.UnsupportedOperation

    with pytest.raises(AttributeError):
        FileWrapper(K()).fileno()


def test_save_with_filename():
    """
    Test that ``save_image`` accepts filename strings (not just file objects).
    This is a test for GH-8.

    """
    im = create_image()
    with NamedTemporaryFile() as outfile:
        save_image(im, outfile.name, 'JPEG')


def test_format_normalization():
    """
    Make sure formats are normalized by ``prepare_image()``.
    See https://github.com/matthewwithanm/django-imagekit/issues/262
    """
    im = Image.new('RGBA', (100, 100))
    assert 'transparency' in prepare_image(im, 'gIF')[1]


def test_quiet():
    """
    Make sure the ``quiet`` util doesn't error if devnull is unwriteable.
    See https://github.com/matthewwithanm/django-imagekit/issues/294
    """
    mocked = Mock(side_effect=OSError)
    with patch.object(os, 'open', mocked):
        with quiet():
            pass
