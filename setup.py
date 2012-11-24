from setuptools import setup

setup(name='mousedb',
      version='1.1.1',
      description="MouseDB is a data management and analysis system for experimental animals",
      long_description=open('README.rst').read(),
      author='Dave Bridges',
      author_email='dave.bridges@gmail.com',
      license='BSD 2-Clause License',
      packages=[mousedb,],
      zip_safe=False,
      install_requires=[
          'Django',
          'Sphinx',],
      )
