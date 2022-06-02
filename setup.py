#!/usr/bin/env python3
# setup.py

from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

DESCRIPTION = 'A simple logging package that helps you log colorized messages in Windows console.'
VERSION = '2.1.2'

setup(
    name='log21',
    version=VERSION,
    url='https://github.com/MPCodeWriter21/log21',
    author='CodeWriter21(Mehrad Pooryoussof)',
    author_email='<CodeWriter21@gmail.com>',
    license='Apache-2.0 License',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['webcolors'],
    packages=['log21'],
    keywords=['python', 'log', 'colorize', 'color', 'logging'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
