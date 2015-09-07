#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# readme = open('README.rst').read()
# history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'Cython>=0.21.1',
    'PyYAML>=3.11',
    'numpy>=1.9.1'
]

dependency_links = [
    "-e git+https://github.com/arruda/pymclevel.git@8bf7b3d76479e007a51f3055198a8bcddb626c84#egg=pymclevel",
]

test_requirements = [
    'coverage>=3.7.1',
    'mock>=1.3.0',
    'Cython>=0.21.1',
    'PyYAML>=3.11',
    'numpy>=1.9.1'
]

setup(
    name='custom-mine-pybuildings',
    version='0.1.0',
    description='Some minecraft buildings made with no templates, only programming',
    # long_description=readme + '\n\n' + history,
    author='Felipe Arruda Pontes',
    author_email='contato@arruda.blog.br',
    # url='https://github.com/arruda/minecraft-pybuildings',
    packages=[
        'customine',
    ],
    package_dir={'customine':
                 'customine'},
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependency_links,
    license="BSD",
    zip_safe=False,
    keywords='custom-mine-pybuildings',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)