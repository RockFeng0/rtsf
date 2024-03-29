#! python3
# -*- encoding: utf-8 -*-

import os
import io
import sys
from shutil import rmtree
from rtsf import __about__
from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()
    
install_requires = [
    "PyYAML",
    "Jinja2",
    "colorama",
    "colorlog",
    "urllib3",
]


class UploadCommand(Command):
    """ Build and publish this package.
        Support setup.py upload. Copied from requests_html.
    """

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in green color."""
        print("\033[0;32m{0}\033[0m".format(s))

    def initialize_options(self):
        """ override
        """
        pass

    def finalize_options(self):
        """ override
        """
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Publishing git tags…')
        os.system('git tag v{0}'.format(__about__.__version__))
        os.system('git push --tags')

        sys.exit()
        
setup(
    name=__about__.__title__,
    version=__about__.__version__,
    description=__about__.__short_desc__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=__about__.__autor__,
    author_email=__about__.__author_email__,
    url=__about__.HOME_PAGE,
    license=__about__.__license__,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    packages=find_packages(exclude=()),
    package_data={
        'rtsf': ["templates/*"],
    },
    keywords='test requests locust HTTP api selenium appium uiautomation',
    install_requires=install_requires,
    extras_require={},
    # $ setup.py upload support.
    cmdclass={
        'upload': UploadCommand
    }
)


