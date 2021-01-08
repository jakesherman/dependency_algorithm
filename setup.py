"""This package only supports Python 3.7 or higher
"""

from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))


# Create a long description
# Copied code here from: https://github.com/kdheepak/fono
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ModuleNotFoundError:
    with open(path.join(here, 'README.md')) as f:
        long_description = f.read()


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_requires = parse_requirements('requirements.txt')


__title__ = "dependency_algorithm"
__summary__ = "Automatically identify and order dependencies so that they resolve correctly"
__uri__ = "https://github.com/jakesherman/dependency_algorithm"
__author__ = "Jake Sherman"
__email__ = "jake@jakesherman.com"
__license__ = 'MIT License'
__copyright__ = "2019-2021 Jake Sherman"
__version__ = "0.1"


setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=__license__,
    url=__uri__,
    author=__author__,
    author_email=__email__,
    packages=["dependency_algorithm"],
    install_requires=install_requires,
    download_url='{}/archive/v{}.tar.gz'.format(
        __uri__, __version__),
    keywords=["dependency", "dependencies", "dependency management"],
    python_requires=">=3.7"
)