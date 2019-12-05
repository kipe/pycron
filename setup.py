#!/usr/bin/env python
from setuptools import setup

setup(
    name='pycron',
    version='3.0.0',
    description='Simple cron-like parser, which determines if current datetime matches conditions.',
    author='Kimmo Huoman',
    author_email='kipenroskaposti@gmail.com',
    license='MIT',
    keywords='cron parser',
    url='https://github.com/kipe/pycron',
    packages=[
        'pycron',
    ],
    python_requires='>=3.5',
    tests_require=[
        "arrow>=0.12.0",
        "coverage>=4.4.2",
        "coveralls>=1.2.0",
        "Delorean>=0.6.0",
        "nose>=1.0",
        "pendulum>=1.3.2",
        "pytz>=2017.3",
        "udatetime>=0.0.14"
    ]
)
