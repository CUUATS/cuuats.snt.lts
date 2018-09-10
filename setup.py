# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '0.1.0'

setup(name='cuuats.snt.lts',
      version=version,
      description='Level of Traffic Stress for the Sustainable Neigborhood Toolkit',
      long_description='\n'.join([open(f).read() for f in [
          'README.md',
          'HISTORY.rst'
      ]]),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Win32 (MS Windows)',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Topic :: Database',
          'Topic :: Scientific/Engineering :: GIS',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='Sustainable Neigborhood Traffic Stress',
      author='Edmond Lai',
      author_email='klai@ccrpc.org',
      url='https://cuuats.org/',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cuuats', 'cuuats.snt'],
      install_requires=[
        'pandas>=0.23.4',
        'numpy>=1.15.1'
      ]
      )
