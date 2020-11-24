from setuptools import setup

import brainutils

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django_brain_utils',
    version=brainutils.__version__,
    description=brainutils.__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=brainutils.__keywords__,
    author=brainutils.__author__,
    author_email=brainutils.__email__,
    url=brainutils.__url__,
    license=brainutils.__license__,
    python_requires='>=3.5',
)