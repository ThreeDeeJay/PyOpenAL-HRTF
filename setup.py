"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import sys

platform = None

if (len(sys.argv) == 4):
    print(sys.argv)
    if (sys.argv[3] == "win-amd64"):
        platform = 64
    elif (sys.argv[3] == "win32"):
        platform = 32

here = path.abspath(path.dirname(__file__))

setup(
    name='PyOpenAL-HRTF',
    
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.7.11a1',

    description='OpenAL integration for Python',
    long_description=open(path.join(here, 'README.md')).read(),
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/Zuzu-Typ/PyOpenAL',

    # Author details
    author='Zuzu_Typ',
    author_email='zuzu.typ@gmail.com',

    # Choose your license
    license='Unilicense',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Games/Entertainment',

        # Pick your license as you wish (should match "license" above)
        'License :: Public Domain',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    # What does your project relate to?
    keywords='OpenAL 3D game Xiph ogg vorbis opus sound playback audio',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    package_data={
        # include shared libraries in wheel packages
        'openal': ['soft_oal_{}.dll'.format(platform)]
    } if platform else {},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[]
)
