"""Setup script for CadQuery - A parametric 3D CAD scripting framework."""

from setuptools import setup, find_packages
import os

# Read the long description from README if available
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'CadQuery - A parametric 3D CAD scripting framework built on top of OCCT.'

# Read version from package
def get_version():
    version_file = os.path.join(here, 'cadquery', 'version.py')
    if os.path.exists(version_file):
        with open(version_file) as f:
            exec_globals = {}
            exec(f.read(), exec_globals)
            return exec_globals.get('__version__', '0.0.0')
    return '0.0.0'


setup(
    name='cadquery',
    version=get_version(),
    description='A parametric 3D CAD scripting framework built on top of OCCT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/CadQuery/cadquery',
    license='Apache Software License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering',],
    keywords='3d cad parametric scripting occt',
_requires=[
        'O],
    extras': [
            'pytest',n            'flake8',
            'mypy',
            'sphinx',
            'sphinx-rtd-theme',
        ],
        'ipython': [
            'jupyter',
            'ipython',
        ],
    },
    entry_points={
        'console_scripts': [
            'cq-editor=cadquery.cq_editor:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
