#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
	'beautifulsoup4',
	'lxml',
        'soupsieve'
]

test_requirements = [
]

setup(
    name='google-search',
    version='1.1.0',
    description="Library for scraping google search results",
    long_description=readme + '\n\n' + history,
    author="Anthony Hseb",
    author_email='anthony.hseb@hotmail.com',
    url='https://github.com/anthonyhseb/googlesearch',
    packages=[
        'googlesearch',
    ],
    package_dir={'googlesearch':
                 'googlesearch'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='googlesearch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
