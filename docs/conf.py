# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # So Sphinx can find your code

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",  # For Markdown support
]

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'show-inheritance': True,
}

# MyST parser settings for better Markdown rendering
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_image",
]

# Project information
project = 'AI Building Blocks'
copyright = '2025, Matthieu Vincke'
author = 'Matthieu Vincke'
release = '1.0.0'

# General configuration
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# Use the Furo theme for a modern, professional look
html_theme = 'furo'

# Theme options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2962ff",
        "color-brand-content": "#2962ff",
        "color-admonition-background": "rgba(41, 98, 255, 0.1)",
    },
    "dark_css_variables": {
        "color-brand-primary": "#448aff",
        "color-brand-content": "#448aff",
        "color-admonition-background": "rgba(68, 138, 255, 0.1)",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

# HTML settings
html_title = 'AI Building Blocks Documentation'
html_short_title = 'AI Building Blocks'
html_static_path = ['_static']
html_favicon = None  # Add a favicon path if you have one
html_logo = None     # Add a logo path if you have one

# GitHub Pages configuration
html_baseurl = 'https://matthieu-vincke.github.io/ai_building_blocks/'

# Add custom CSS for additional styling
html_css_files = [
    'custom.css',
]

# Show source links
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# -- Extension configuration -------------------------------------------------

# Intersphinx mapping for linking to other projects
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'langchain': ('https://python.langchain.com/', None),
}

# Napoleon settings for Google and NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
