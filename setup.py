import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read

setup(
    name = "mousedb",
    version = "0.2.1dev",
    url = 'http://github.com/davebridges/mousedb',
    license = 'BSD',
    description = "A web based application for storage and organization of data regarding experimental animals",
    long_description = read('README.rst'),
    author = 'Dave Bridges',
    author_email = 'dave.bridges@gmail.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'south', 'django-ajax-selects', 'mysql-python'],

classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
