# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../app/'))
sys.path.insert(0, os.path.abspath('../app/utils/'))
sys.path.insert(0, os.path.abspath('../app/controllers/'))
sys.path.insert(0, os.path.abspath('../app/controllers/auth_controllers/'))
sys.path.insert(0, os.path.abspath('../app/controllers/business_controllers/'))
sys.path.insert(0, os.path.abspath('../app/controllers/business_controllers/customer_controllers/'))
sys.path.insert(0, os.path.abspath('../app/controllers/business_controllers/contract_controllers/'))
sys.path.insert(0, os.path.abspath('../app/controllers/business_controllers/event_controllers/'))
sys.path.insert(0, os.path.abspath('../app/controllers/first_init_database/'))
sys.path.insert(0, os.path.abspath('../app/controllers/user_controllers/'))
sys.path.insert(0, os.path.abspath('../app/controllers/user_controllers/collaborator_controllers/'))
sys.path.insert(0, os.path.abspath('../app/controllers/utils_controllers/'))
sys.path.insert(0, os.path.abspath('../app/models/'))
sys.path.insert(0, os.path.abspath('../app/models/database_models/'))
sys.path.insert(0, os.path.abspath('../app/models/class_models/'))
sys.path.insert(0, os.path.abspath('../app/models/class_models/business_models/'))
sys.path.insert(0, os.path.abspath('../app/models/class_models/user_models/'))
sys.path.insert(0, os.path.abspath('../app/views/'))
sys.path.insert(0, os.path.abspath('../app/views/class_views/'))
sys.path.insert(0, os.path.abspath('../app/views/general_views/'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Project12'
copyright = '2023, Nicolas Deleu'
author = 'Nicolas Deleu'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx_click']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
