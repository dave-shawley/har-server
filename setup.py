#!/usr/bin/env python
#
import setuptools

import harserver

setuptools.setup(
    name='har-server',
    version=harserver.version,
    description='Programmable HTTP server for testing',
    long_description=open('README.rst').read(),
    url='https://github.com/dave-shawley/har-server',
    author='Dave Shawley',
    author_email='daveshawley+harserver@gmail.com',
    packages=['harserver'],
    install_requires=[
        'aiohttp==3.4.4',
        'yarl==1.3.0',
    ],
    extras_require={
        'dev': [
            'coverage==4.5.2',
            'coveralls==1.5.1',
            'flake8==3.6.0',
            'nose==1.3.7',
            'pycodestyle==2.4.0',
            'pyflakes==2.0.0',
            'Sphinx==1.8.2',
            'twine==1.12.1',
            'wheel==0.32.3',
            'yapf==0.25.0',
        ],
        'docs': [
            'Sphinx==1.8.2',
        ],
    },
    project_urls={
        'Builds':
            'https://circleci.com/gh/dave-shawley/har-server/',
        'Coverage Reports':
            'https://coveralls.io/github/dave-shawley/har-server',
        'Documentation':
            'http://har-server.readthedocs.io/',
        'Source Code':
            'https://github.com/dave-shawley/har-server/',
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: No Input/Output (Daemon)',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Testing :: Mocking',
    ],
)
