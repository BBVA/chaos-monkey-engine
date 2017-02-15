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
      install_requires=[
            'apscheduler==3.3.1',
            'click==6.7',
            'apache-libcloud==1.5.0',
            'paramiko==2.1.1',
            'requests==2.13.0',
            'arrow==0.10.0',
            'flask==0.12',
            'flask-cors==3.0.2',
            'flask_sqlalchemy==2.1',
            'gevent==1.2.1',
            'SQLAlchemy==1.1.5',
            'jsonschema==2.6.0',
            'flask-hal-bbva==1.0.5'
      ],
      entry_points='''
      [console_scripts]
      chaos-monkey-engine=chaosmonkey.cm:cm
      ''')
