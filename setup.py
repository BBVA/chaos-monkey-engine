from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(name='chaosmonkey',
      version=version,
      description='A Chaos Engineering swiss army knife',
      author='BBVALabs',
      long_description=long_description,
      url="https://github.com/BBVA/chaos-monkey-engine",
      packages=find_packages(),
      include_package_data=True,
      entry_points='''
        [console_scripts]
        chaos-monkey-engine=chaosmonkey.cm:cm
        ''',
      )
