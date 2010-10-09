from setuptools import setup, find_packages

setup(
    name = "django-mousedb",
    version = "0.2",
    url = 'http://github.com/davebridges/mousedb',
    license = 'BSD',
    description = "A web based application for storage and organization of data regarding experimental animals",
    author = 'Dave Bridges',
    author_email = 'dave.bridges@gmail.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],

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
