"""Setup script to create the project or create a distribution tar.gz file."""
import os
from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

BASE_DIR = os.getcwd()


class PreDevelopCommand(develop):
    """Pre-installation for development mode."""

    def run(self):
        """Execute a script."""
        develop.run(self)


class PreInstallCommand(install):
    """Pre-installation for install mode."""

    def run(self):
        """Execute the preinstall functions."""
        self.create_log_dir()
        install.do_egg_install(self)

    def create_log_dir(self):
        """Create the logs folder inside the root application app."""
        log_dir = 'api/logs'
        dir = os.path.join(BASE_DIR, log_dir)
        # create directories, if exists don't throw an exception
        os.makedirs(dir, exist_ok=True)


def read(fname):
    """Open the file provided as an argument."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='FedalRestfulAPI',
    version='3.0',
    description='private resutful api',
    author='Omar Aljazairy',
    author_email='omar@fedal.nl',
    keywords='fedal api',
    url='http://fedal.net',
    long_description=read('README.md'),
    install_requires=[read('requirements.txt')],
    packages=find_packages(include=['api.api', 'api.spanglish', 'api.tests']),
    package_data={
        # If any package contains *.txt or *.rst files,
        # include them:
        # "": ["*.txt", "*.rst"],
        # And include any *.msg files found in the "hello"
        # package, too:
        # "hello": ["*.msg"],
    },
    zip_safe=True,
    python_requires='>=3.6',
    cmdclass={
        'develop': PreDevelopCommand,
        'install': PreInstallCommand,
    },
)
