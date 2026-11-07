import datetime
import os
import sphinx_epytext
import sys

sys.path.insert(0, os.path.abspath('../python3'))
import pyinotify

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyinotify'
author = 'Sebastien Martini'
copyright = f'{datetime.datetime.now().year}, {author}'
release = pyinotify.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
'sphinx.ext.autodoc',
# your other sphinx extensions
# ...
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pyramid'
html_static_path = ['_static']
#


def setup(app):
    app.connect('autodoc-process-docstring', sphinx_epytext.process_docstring)
