#!/usr/bin/python

import os

from setuptools import setup, find_packages

# --- Setuptools Configuration Parameters --- #
CONFIG = dict()
CONFIG['name'] = 'cloudcarver'
CONFIG['description'] = 'AWS Cloudformation Custom Resource Framework'
CONFIG['author'] = 'Jason Denning'
CONFIG['author_email'] = 'jason@ngeniux.com'

LICENSE_FILE = 'LICENSE.txt'
VERSION_FILE = 'VERSION.txt'
README_FILE = 'README.rst'
CHANGES_FILE = 'CHANGES.rst'


CONFIG['test_suite'] = '.'.join([CONFIG['name'], 'tests'])

# Path to parent directory of this file
here = os.path.abspath(os.path.dirname(__file__))

# Scan directory for packages; may also be specified as a list
CONFIG['packages'] = find_packages()

# Setuptools parameters to include from files - given as a list of tuples,
# where each tuple has the form: (parameter_name, file_name, default_value)
metadata_files = {
    ('license', LICENSE_FILE, 'Proprietary'),
    ('version', VERSION_FILE, '1.0'),
    ('readme', README_FILE, ''),
    ('changes', CHANGES_FILE, ''),
}

# Load params from metadata files, if they exist; otherwise use default value
for param in metadata_files:
    param_name = param[0]
    file_name = param[1]
    default_value = param[2]
    try:
        with open(os.path.join(here, file_name), 'r') as f:
            CONFIG[param_name] = f.read()
    except IOError:
        # Could not load external file, use the default value for the param
        CONFIG[param_name] = default_value


# --- Requirements -- #

with open('requirements.txt', 'r') as req_file:
    install_requires = [line.strip() for line in req_file.readlines()]

docs_extras_requires = []

testing_requires = [
    'nose',
    'mock',
]

testing_extras_requires = testing_requires + [
    'coverage'
]

# --- End of Requirements --- #

setup(
    name=CONFIG.get('name'),
    version=CONFIG.get('version'),
    description=CONFIG.get('description'),
    long_description=CONFIG.get('readme') + '\n\n' + CONFIG.get('changes'),
    author=CONFIG.get('author'),
    author_email=CONFIG.get('author_email'),
    url=CONFIG.get('url'),
    license=CONFIG.get('license'),
    packages=CONFIG.get('packages'),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras_requires,
        'docs': docs_extras_requires,
    },
    tests_require=testing_requires,
    test_suite=CONFIG.get('test_suite'),
)
