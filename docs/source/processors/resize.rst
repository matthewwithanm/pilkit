
Resize
=======

Original Image

.. image:: ../_ext/original.jpg


Resize To Fill
---------------
.. pil-block::

    from pilkit.processors.resize import ResizeToFill

    old_img = Image.open('original.jpg')
    resizer = ResizeToFill(300, 300)
    new_img = resizer.process(old_img)

.. pil-block::

    from pilkit.processors.resize import ResizeToFill

    old_img = Image.open('original.jpg')
    resizer = ResizeToFill(600, 300)
    new_img = resizer.process(old_img)

.. pil-block::

    from pilkit.processors.resize import ResizeToFill

    old_img = Image.open('original.jpg')
    resizer = ResizeToFill(300, 600)
    new_img = resizer.process(old_img)


Resize To Cover
----------------
.. pil-block::

    from pilkit.processors.resize import ResizeToCover

    old_img = Image.open('original.jpg')
    resizer = ResizeToCover(300, 300)  # width, height
    new_img = resizer.process(old_img)

.. pil-block::

    from pilkit.processors.resize import ResizeToCover

    old_img = Image.open('original.jpg')
    resizer = ResizeToCover(600, 300)  # width, height
    new_img = resizer.process(old_img)

.. pil-block::

    from pilkit.processors.resize import ResizeToCover

    old_img = Image.open('original.jpg')
    resizer = ResizeToCover(300, 600)  # width, height
    new_img = resizer.process(old_img)


Resize To Fit
--------------
.. pil-block::

    from pilkit.processors.resize import ResizeToFit

    old_img = Image.open('original.jpg')
    resizer = ResizeToFit(300, 300)
    new_img = resizer.process(old_img)

.. pil-block::

    from pilkit.processors.resize import ResizeToFit

    old_img = Image.open('original.jpg')
    resizer = ResizeToFit(600, 300)
    new_img = resizer.process(old_img)

.. pil-block::

    from pilkit.processors.resize import ResizeToFit

    old_img = Image.open('original.jpg')
    resizer = ResizeToFit(300, 600)
    new_img = resizer.process(old_img)


Thumbnail
----------
.. pil-block::

    from pilkit.processors.resize import Thumbnail

    old_img = Image.open('original.jpg')
    resizer = Thumbnail(300, 300)
    new_img = resizer.process(old_img)

.. pil-block::

    from pilkit.processors.resize import Thumbnail

    old_img = Image.open('original.jpg')
    resizer = Thumbnail(600, 300)
    new_img = resizer.process(old_img)

.. pil-block::

    from pilkit.processors.resize import Thumbnail

    old_img = Image.open('original.jpg')
    resizer = Thumbnail(300, 600)
    new_img = resizer.process(old_img)
