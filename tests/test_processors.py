from pilkit.lib import Image, ImageDraw
from pilkit.processors import (Resize, ResizeToFill, ResizeToFit, SmartCrop,
                               SmartResize)
from nose.tools import eq_, assert_true
from pilkit.processors.resize import Thumbnail
from .utils import create_image
import mock


def test_smartcrop():
    img = SmartCrop(100, 100).process(create_image())
    eq_(img.size, (100, 100))


def test_resizetofill():
    img = ResizeToFill(100, 100).process(create_image())
    eq_(img.size, (100, 100))


def test_resizetofit():
    # First create an image with aspect ratio 2:1...
    img = Image.new('RGB', (200, 100))

    # ...then resize it to fit within a 100x100 canvas.
    img = ResizeToFit(100, 100).process(img)

    # Assert that the image has maintained the aspect ratio.
    eq_(img.size, (100, 50))


def test_resize_rounding():
    """
    Regression test for matthewwithanm/pilkit#1
    """

    img = Image.new('RGB', (95, 95))
    img = ResizeToFill(28, 28).process(img)
    eq_(img.size, (28, 28))


def test_resizetofit_mat():
    img = Image.new('RGB', (200, 100))
    img = ResizeToFit(100, 100, mat_color=0x000000).process(img)
    eq_(img.size, (100, 100))


def test_resize_antialiasing():
    """
    Test that the Resize processor antialiases.

    The Resize processor is used by all of the Resize* variants, so this should
    cover all of resize processors. Basically, this is to test that it converts
    to RGBA mode before resizing.

    Related: jdriscoll/django-imagekit#192

    """
    # Create a palette image and draw a circle into it.
    img = Image.new('P', (500, 500), 1)
    img.putpalette([
        0,   0,   0,
        255, 255, 255,
        0,   0,   255,
    ])
    d = ImageDraw.ImageDraw(img)
    d.ellipse((100, 100, 400, 400), fill=2)

    # Resize the image using the Resize processor
    img = Resize(100, 100).process(img)

    # Count the number of colors
    color_count = len(list(filter(None, img.histogram())))

    assert_true(color_count > 2)


def test_upscale():
    """
    Test that the upscale argument works as expected.

    """

    img = Image.new('RGB', (100, 100))

    for P in [Resize, ResizeToFit, ResizeToFill, SmartResize]:
        img2 = P(500, 500, upscale=True).process(img)
        eq_(img2.size, (500, 500))

        img2 = P(500, 500, upscale=False).process(img)
        eq_(img2.size, (100, 100))


def test_should_raise_exception_if_anchor_is_passed_and_crop_is_set_to_false():
    try:
        Thumbnail(height=200, width=200, upscale=False, crop=False, anchor='t')
    except Exception as e:
        eq_(str(e), "You can't specify an anchor point if crop is False.")


def test_should_set_crop_to_true_if_anchor_is_passed_without_crop():
    thumb = Thumbnail(height=200, width=200, upscale=False, anchor='t')
    assert_true(thumb.crop)


def test_should_raise_exception_when_crop_is_passed_without_height_and_width():
    img = Image.new('RGB', (100, 100))
    try:
        Thumbnail(crop=True).process(img)
    except Exception as e:
        eq_(str(e), 'You must provide both a width and height when cropping.')


@mock.patch('pilkit.processors.resize.SmartResize')
def test_should_call_smartresize_when_crop_not_passed(my_mock):
    img = Image.new('RGB', (100, 100))
    Thumbnail(height=200, width=200, upscale=False).process(img)
    assert_true(my_mock.called)


@mock.patch('pilkit.processors.resize.SmartResize')
def test_should_repass_upscale_option_true(my_mock):
    img = Image.new('RGB', (100, 100))
    Thumbnail(height=200, width=200, upscale=True).process(img)
    my_mock.assert_called_once_with(width=200, upscale=True, height=200)


@mock.patch('pilkit.processors.resize.SmartResize')
def test_should_repass_upscale_option_false(my_mock):
    img = Image.new('RGB', (100, 100))
    Thumbnail(height=200, width=200, upscale=False).process(img)
    my_mock.assert_called_once_with(width=200, upscale=False, height=200)


@mock.patch('pilkit.processors.resize.ResizeToFill')
def test_should_call_resizetofill_when_crop_and_ancho_is_passed(my_mock):
    img = Image.new('RGB', (100, 100))
    Thumbnail(height=200, width=200, anchor='fake').process(img)
    assert_true(my_mock.called)

@mock.patch('pilkit.processors.resize.ResizeToFit')
def test_should_call_resizetofit_when_crop_is_not_passed(my_mock):
    img = Image.new('RGB', (100, 100))
    Thumbnail(height=200, width=200, crop=False).process(img)
    assert_true(my_mock.called)
