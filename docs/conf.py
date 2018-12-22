# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import harserver
project = 'HAR Server'
copyright = '2018, Dave Shawley'
author = 'Dave Shawley'
version = '.'.join(str(c) for c in harserver.version_info[:2])
release = harserver.version
needs_sphinx = '1.8'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
pygments_style = None
html_theme = 'alabaster'
html_theme_options = {
    'github_user': 'dave-shawley',
    'github_repo': 'har-server',
    'description': 'Programmable HTTP server for testing',
    'fixed_sidebar': True,
    'github_button': True,
}
html_sidebars = {}
intersphinx_mapping = {
    'https://docs.python.org/': None,
}
