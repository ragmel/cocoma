#Copyright 2012 SAP Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# This is part of the COCOMA framework
#
# COCOMA is a framework for COntrolled COntentious and MAlicious patterns
#

import os

import distribute_setup
distribute_setup.use_setuptools()

#from setup_helpers import (description, get_version, long_description, require_python)
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


#require_python(0x20600f0)
#__version__ = get_version('__init__.py')
#__version__ = '0.1'
#try:
#     import pkgutil
#     data = pkgutil.get_data(__name__, 'cocoma/data/cocoma.sqlite')
#except ImportError:
#     import pkg_resources
#     data = pkg_resources.resource_string(__name__, 'cocoma/data/cocoma.sqlite')

setup(
    name='cocoma',
    version='0.1',
    #package_dir = {'':''},
    py_modules=['cocoma','bin','distributions'],
    #packages = [''],
    #namespace_packages=['COCOMA'],
    packages=find_packages(),
    #package_data={'cocoma': ['LICENSE', 'NEWS', 'cocoma/data/cocoma.sqlite']},
    include_package_data=True,
    maintainer='Carmelo Ragusa',
    maintainer_email='carmelo.ragusa@sap.com',
    description=read('cocoma/README'),
    long_description=read('cocoma/NEWS'),
    license='Apachev2',
    url='http://sourgeforce.net',
    download_url='https://sourgeforce.net/download',
    #test_suite='COCOMA.tests',
    keywords="Controlled contentious malicious faulty framework patterns",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
	'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
