# Configuration file for the Sphinx documentation builder.
# -- Project information
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

from flask_utils import __version__  # noqa: E402


project = "Flask-Utils"
copyright = "2024, Jules Lasne"


release = __version__
version = __version__

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    # notfound causes a bug with the flask theme, see https://github.com/readthedocs/sphinx-notfound-page/issues/148
    # "notfound.extension",
    "pallets_sphinx_themes",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "flask"

# -- Options for EPUB output
epub_show_urls = "footnote"

add_module_names = False