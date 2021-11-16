#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
"xlrd==1.2.0",
"swolfpy_inputdata",
"swolfpy_processmodels",
"bw-migrations==0.1",
"bw2analyzer==0.9.4",
"bw2calc==1.8.0",
"bw2data==3.6.2",
"bw2io==0.7.12.1",
"bw2parameters==0.6.6",
"brightway2==2.3",
"PySide2==5.14",
"plotly",
"graphviz",
"pyDOE",
"pytest",
"pytest-cov",
"pytest-flake8",
"coverage",
]

setup_requirements = [ ]

package_input_data = {'swolfpy':['SWOLF_LCIA_Methods.csv']}
                                                                

test_requirements = [ ]

files = None


setup(
    author="Mojtaba Sardarmehni",
    author_email='msardar2@ncsu.edu',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Natural Language :: English',
    ],
    description="Solid Waste Optimization Life-cycle Framework in Python(SwolfPy)",
    install_requires=requirements,
    license="GNU GENERAL PUBLIC LICENSE V2",
    long_description=readme + '\n\n' + history,
    long_description_content_type= 'text/x-rst',
    include_package_data=True,
    keywords='swolfpy',
    name='swolfpy',
    packages=find_packages(include=['swolfpy', 'swolfpy.*']),
    setup_requires=setup_requirements,
    package_data=package_input_data,
    data_files = files,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SwolfPy-Project/swolfpy',
    version='0.2.3',
    zip_safe=False,
)
