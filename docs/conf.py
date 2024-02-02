from __future__ import annotations

import os
import sys
from datetime import date

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_path)

from icometrix_sdk._version import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "icometrix-sdk"
copyright = f"{date.today().year}, icometrix"
author = "icometrix"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc"
]

# sphinx.ext.autodoc options
autodoc_default_options = {
    'exclude-members': 'model_config, model_fields'  # exclude pydantic internal fields
}

templates_path = ["_templates"]
exclude_patterns = []

# Show typehints as content of the function or method
autodoc_typehints = "description"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
