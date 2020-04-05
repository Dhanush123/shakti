"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from shakti import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='shakti',
    packages=find_packages(),
    version=__version__,
    description='CLI for the Shakti ML deployment platform written in Python',
    long_description=long_description,
    url='https://github.com/Dhanush123/shakti',
    download_url='https://github.com/Dhanush123/shakti/archive/0.1.0.tar.gz',
    author='Dhanush Patel',
    author_email='dhanushpatel101@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3'
    ],
    keywords='cli',
    entry_points={
        'console_scripts': [
            'shakti=shakti.cli:main',
        ],
    },
    python_requires='>=3.0',
    install_requires=[
        "autopep8",
        "fire",
        "firebase-admin",
        "google-cloud-dataproc",
        "pylint",
        "pyspark",
        "python-dotenv",
        "rope",
        "scikit-learn",
        "tensorflow"
    ]
)
