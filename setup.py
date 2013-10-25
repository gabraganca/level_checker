"""
Install package.
"""

from distutils.core import setup
import os

HOME = os.getenv('HOME')

setup(name="levelchecker",
      description="Synspec Level Checker",
      long_description=open('README.md').read(),
      author="Gustavo de Almeida Braganca",
      author_email="ga.braganca@gmail.com",
      download_url='http://github.com/gabraganca/level_checker',
      license='MIT',
      version='0.0.1',
      scripts=["scripts/levelchecker"],
      packages=['levelchecker'],
      data_files=[(HOME + '/.levelchecker/',
                   ['datafiles/chemical_elements.json'])],
      classifiers=[
        'Development Status :: Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Astronomy'],
    )
