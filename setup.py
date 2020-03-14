#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
"brightway2",
"jupyter",
"PySide2",
"pandas"
]

setup_requirements = [ ]

package_input_data = {'swolfpy.Data':['AD_Input.csv',
                                'CommonData.csv',
                                'Composting_Input.csv',
                                'LF_Gas_emission_factors.csv',
                                'LF_Input.csv',
                                'LF_Leachate_Allocation.csv',
                                'LF_Leachate_Coeff.csv',
                                'SF_collection_Input.csv',
                                'SF_collection_Input-Material_dependent.csv',
                                'SF_input_col.csv',
                                'SS_MRF_Input.csv',
                                'SWOLF _ IPPC.csv',
                                'SWOLF_AccountMode_LCI DATA.csv',
                                'WTE_Input.csv',
                                'LF_Gas_emission_factors.xlsx',
                                'LF_Leachate_Allocation.xlsx',
                                'Material properties - process modles.xlsx',
                                'Material properties.xlsx']}
                                                                

test_requirements = [ ]

files = None


setup(
    author="Mojtaba Sardarmehni",
    author_email='msardar2@ncsu.edu',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description="Solid Waste Optimization Life-cycle Framework in Python(SwolfPy)",
    install_requires=requirements,
    license="GNU GENERAL PUBLIC LICENSE V2",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='SwolfPy',
    name='swolfpy',
    packages=find_packages(include=['sowlfpy', 'swolfpy.*']),
    setup_requires=setup_requirements,
    package_data=package_input_data,
    data_files = files,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://bitbucket.org/swolfpy/swolfpy',
    version='0.1.2',
    zip_safe=False,
)
