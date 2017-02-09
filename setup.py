from setuptools import setup, find_packages

setup(name='chaosmonkey',
      version='1.0',
      description='',
      author='BBVALabs',
      packages=find_packages(),
      include_package_data=True,
      entry_points='''
        [console_scripts]
        chaos-monkey-engine=chaosmonkey.cm:cm
        ''',
     )
