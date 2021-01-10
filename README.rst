PILKit is a collection of utilities for working with PIL (the Python Imaging
Library).

One of its main features is a set of **processors** which expose a simple
interface for performing manipulations on PIL images.

Looking for more advanced processors? Check out `Instakit`_!

**For the complete documentation on the latest stable version of PILKit, see**
`PILKit on RTD`_.

.. image:: https://github.com/matthewwithanm/pilkit/workflows/Python%20CI/badge.svg
  :target: https://github.com/matthewwithanm/pilkit/actions?query=workflow%3A%22Python+CI%22

.. _`PILKit on RTD`: http://pilkit.readthedocs.org
.. _`Instakit`: https://github.com/fish2000/instakit


Installation
============

1. Install `PIL`_ or `Pillow`_.
2. Run ``pip install pilkit`` (or clone the source and put the pilkit module on
   your path)

.. note:: If you've never seen Pillow before, it considers itself a
   more-frequently updated "friendly" fork of PIL that's compatible with
   setuptools. As such, it shares the same namespace as PIL does and is a
   drop-in replacement.

.. _`PIL`: http://pypi.python.org/pypi/PIL
.. _`Pillow`: http://pypi.python.org/pypi/Pillow


Usage Overview
==============


Processors
----------

The "pilkit.processors" module contains several classes for processing PIL
images, which provide an easy to understand API:

.. code-block:: python

    from pilkit.processors import ResizeToFit

    img = Image.open('/path/to/my/image.png')
    processor = ResizeToFit(100, 100)
    new_img = processor.process(img)

A few of the included processors are:

* ``ResizeToFit``
* ``ResizeToFill``
* ``SmartResize``
* ``Adjust``
* ``TrimBorderColor``
* ``Transpose``

There's also a ``ProcessorPipeline`` class for executing processors
sequentially:

.. code-block:: python

    from pilkit.processors import ProcessorPipeline, ResizeToFit, Adjust

    img = Image.open('/path/to/my/image.png')
    processor = ProcessorPipeline([Adjust(color=0), ResizeToFit(100, 100)])
    new_image = processor.process(img)


Utilities
---------

In addition to the processors, PILKit contains a few utilities to ease the pain
of working with PIL. Some examples:

``prepare_image``
    Prepares the image for saving to the provided format by doing some
    common-sense conversions, including preserving transparency and quantizing.
``save_image``
    Wraps PIL's ``Image.save()`` method in order to gracefully handle PIL's
    "Suspension not allowed here" errors, and (optionally) prepares the image
    using ``prepare_image``

Utilities are also included for converting between formats, extensions, and
mimetypes.


Community
=========

Please use `the GitHub issue tracker <https://github.com/matthewwithanm/pilkit/issues>`_
to report bugs. `A mailing list <https://groups.google.com/forum/#!forum/django-imagekit>`_
also exists to discuss the project and ask questions, as well as the official
`#imagekit <irc://irc.freenode.net/imagekit>`_ channel on Freenode. (Both of
these are shared with the `django-imagekit`_ project—from which PILKit spun
off.)

.. _`django-imagekit`: https://github.com/jdriscoll/django-imagekit
