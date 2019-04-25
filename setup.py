from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pspring',
    version='0.0.17',
    license='TBD',
    author='Vasudevan Palani',
    author_email='vasudevan.palani@gmail.com',
    url='https://github.com/vasudevan-palani/pspring',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pspring','pspring.core'],
    include_package_data=True,
    description="A framework inspired by spring for python",
)
