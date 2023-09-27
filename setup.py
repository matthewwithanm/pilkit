#!/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages


def read(filepath):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        return f.read()


# Load package meta from the pkgmeta module without loading the package.
pkgmeta = {}
pkgmeta_file = os.path.join(os.path.dirname(__file__), 'pilkit', 'pkgmeta.py')
with open(pkgmeta_file) as f:
    code = compile(f.read(), 'pkgmeta.py', 'exec')
    exec(code, pkgmeta)


setup(
    name='pilkit',
    version=pkgmeta['__version__'],
    description='A collection of utilities and processors for the Python Imaging Library.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    author='Matthew Tretter',
    author_email='m@tthewwithanm.com',
    license='BSD',
    url='http://github.com/matthewwithanm/pilkit/',
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Pillow>=7.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities'
    ],
)
