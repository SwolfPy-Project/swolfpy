.. General

================================================================
Solid Waste Optimization Life-cycle Framework in Python(swolfpy)
================================================================

.. image:: https://img.shields.io/pypi/v/swolfpy.svg
        :target: https://pypi.python.org/pypi/swolfpy
        
.. image:: https://img.shields.io/pypi/pyversions/swolfpy.svg
    :target: https://pypi.org/project/swolfpy/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/swolfpy.svg
    :target: https://pypi.org/project/swolfpy/
    :alt: License

.. image:: https://img.shields.io/pypi/format/swolfpy.svg
    :target: https://pypi.org/project/swolfpy/
    :alt: Format

.. image:: https://readthedocs.org/projects/swolfpy/badge/?version=latest
        :target: https://swolfpy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


* Free software: GNU GENERAL PUBLIC LICENSE V2
* Documentation: https://swolfpy.readthedocs.io.
* Repository: https://bitbucket.org/swolfpy/swolfpy
* Other links: 
        https://go.ncsu.edu/swolfpy

        https://jwlevis.wixsite.com/swolf


Features
--------

* Life cycle assessment of Municipal Solid Waste (MSW) systems. Process models include Landfill, Waste-to-Energy (WTE), Composting, Anaerobic Digestion (AD), Single Stream Material Recovery Facility (MRF), Reprocessing, and Collection.
* Monte Carlo simulation
* Optimization


.. Installation

Installation
------------
1- Download and install miniconda from:  https://docs.conda.io/en/latest/miniconda.html

2- Update conda in a terminal window or anaconda prompt::

        conda update conda

3- Add conda channels::

        conda config --append channels conda-forge
        conda config --append channels cmutel
        conda config --append channels haasad

4- Create a new environment for PySWOLF::

        conda create --name swolfpy python=3.7

5- Activate the environment::

        conda activate swolfpy

6- Install PySWOLF in the environment::

        pip install swolfpy

7- Open python to run swolfpy::

        ipython

8- Run swolfpy in python::

        from swolfpy import *
        swolfpy()

.. endInstallation
