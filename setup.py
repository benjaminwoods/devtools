"""
devtools setup.py.

Requires Python >= 3.7.
"""

import sys

from setuptools import setup

if sys.version_info < (3, 7):
    raise NotImplementedError('devtools requires Python >= 3.7.')

setup(
    name="devtools",
    version="0.0.1",

    package_dir={'':'src'},
    packages=['devtools'],
    install_requires=[],

    # Metadata
    author="Benjamin Woods",
    author_email="ben@bjqw.me",
    description="Tools to aid Python development.",
    keywords="development tools",
    url="https://github.com/benjaminwoods/devtools",
    project_urls={},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Typing :: Typed"
    ]
)
