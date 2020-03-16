"""Setup  script to create the project or create a distribution tar.gz file."""
import os
from distutils.core import setup


def read(fname):
    """Open the file provided as an argument."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Fedal Restful API',
    version='3.0',
    description='private resutful api',
    author='Omar Aljazairy',
    author_email='omar@fedal.nl',
    url='http://fedal.net',
    long_description=read('README.md'),
    packages=['api.api', 'api.spanglish', 'api.tests'],
    package_dir={},
)
