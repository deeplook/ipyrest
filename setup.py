#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = open('requirements.txt').read().strip().split('\n')

setup_requirements = ['pytest-runner', ]

test_requirements = requirements + ['pytest', ]

setup(
    author="Dinu Gherman",
    author_email='@'.join(['gherman', 'darwin.in-berlin.de']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="An emerging widget for exploring RESTful APIs in Jupyter notebooks.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='ipyrest',
    name='ipyrest',
    packages=find_packages(include=['ipyrest']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/deeplook/ipyrest',
    version='0.1.2',
    zip_safe=False,
)
