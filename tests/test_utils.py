from pilkit.exceptions import UnknownFormat, UnknownExtension
from pilkit.utils import extension_to_format, format_to_extension
from nose.tools import eq_, raises


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
