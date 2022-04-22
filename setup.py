"""
Setup script for the FlowKit package
"""
from setuptools import setup, find_packages

# read in version string
VERSION_FILE = 'flowkit/_version.py'
__version__ = None  # to avoid inspection warning and check if __version__ was loaded
exec(open(VERSION_FILE).read())

if __version__ is None:
    raise RuntimeError("__version__ string not found in file %s" % VERSION_FILE)

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

reqs = [
    'flowio>=1,<1.1',
    'flowutils>=1,<1.1',
    'matplotlib',
    'scipy',
    'statsmodels',
    'seaborn',
    'pandas',
    'numpy>=1.19',
    'lxml',
    'bokeh>=2,<3',
    'anytree',
    'networkx',
    'psutil'
]

setup(
    name='FlowKit',
    version=__version__,
    packages=find_packages(exclude=["flowkit/tests/"]),
    package_data={'': ['_resources/*.xsd']},
    include_package_data=True,
    description='Flow Cytometry Toolkit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Scott White",
    license='BSD',
    url="https://github.com/whitews/flowkit",
    ext_modules=[],
    install_requires=reqs,
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7'
    ]
)
