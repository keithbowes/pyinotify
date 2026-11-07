import datetime
import sphinx_epytext
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyinotify'
author = 'Sebastien Martini'
copyright = f'{datetime.datetime.now().year}, {author}'
try:
    import pyinotify
    release = pyinotify.pyinotify.__version__
except AttributeError:
    release = 'master'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pyramid'
html_static_path = ['_static']
#
extensions = [
'sphinx.ext.autodoc',
# your other sphinx extensions
# ...
]

def setup(app):
    app.connect('autodoc-process-docstring', sphinx_epytext.process_docstring)
