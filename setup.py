#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages

# Workaround for multiprocessing/nose issue. See http://bugs.python.org/msg170215
try:
    import multiprocessing
except ImportError:
    pass

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

# Load package meta from the pkgmeta module without loading the package.
pkgmeta = {}
pkgmeta_file = os.path.join(os.path.dirname(__file__), 'pilkit', 'pkgmeta.py')
with open(pkgmeta_file) as f:
    code = compile(f.read(), 'pkgmeta.py', 'exec')
    exec(code, pkgmeta)


setup(
    name='pilkit',
    version=pkgmeta['__version__'],
    description='A collection of utilities and processors for the Python Imaging Libary.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    author='Matthew Tretter',
    author_email='m@tthewwithanm.com',
    license='BSD',
    url='http://github.com/matthewwithanm/pilkit/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    tests_require=[
        'mock==1.0.1',
        'nose==1.2.1',
        'nose-progressive==1.3',
        'Pillow',
    ],
    test_suite='nose.collector',
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities'
    ],
)
