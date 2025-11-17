#!/usr/bin/env python3
"""
RRGM FTL Validation Toolkit - Setup Script

Installation:
    pip install -e .

Usage after install:
    rrgm-ftl-validate --all
"""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rrgm-ftl-validation',
    version='1.0.0',
    description='Validation toolkit for Faster-Than-Light transit in the Rozon Recursive Gravity Model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luna (Digital Intelligence) and Daniel Rozon',
    author_email='',
    url='https://github.com/yourusername/rrgm-ftl-validation',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'scipy>=1.7.0',
        'pandas>=1.3.0',
        'matplotlib>=3.5.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
        ],
        'fast': [
            'numba>=0.55.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'rrgm-ftl-validate=run_toolkit:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords='quantum-physics faster-than-light rrgm recursive-gravity validation',
)
