# -*- coding: utf-8 -*-
from setuptools import setup

__author__ = 'Martin Uhrin'
__license__ = 'MIT and CC-BY'

setup(
    name='milad-paper',
    version='2021.04',
    description='Moment Invariants Local Atomic Descriptor Paper',
    long_description=open('README.rst').read(),
    url='https://github.com/muhrin/milad-paper-2021.git',
    author='Martin Uhrin',
    author_email='martin.uhrin.10@ucl.ac.uk',
    license=__license__,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='machine learning, atomic descriptor, moment invariants',
    install_requires=[
        'milad', 'plotly', 'schnetpack'
    ],
    include_package_data=True,
)
