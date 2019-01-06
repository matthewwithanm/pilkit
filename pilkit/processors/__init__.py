# flake8: noqa

"""
PILKit image processors.

A processor accepts an image, does some stuff, and returns the result.
Processors can do anything with the image you want, but their responsibilities
should be limited to image manipulations--they should be completely decoupled
from the filesystem.

"""

from .base import *
from .crop import *
from .convert import *
from .filter import *
from .overlay import *
from .resize import *
