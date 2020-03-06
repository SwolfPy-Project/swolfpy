.. General
=============================================================
Python Solid Waste Optimization Life-cycle Framework(PySWOLF)
=============================================================


.. image:: https://img.shields.io/pypi/v/pyswolf.svg
        :target: https://pypi.python.org/pypi/pyswolf

.. image:: https://readthedocs.org/projects/pyswolf/badge/?version=latest
        :target: https://pyswolf.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



* Free software: BSD license
* Documentation: https://pyswolf.readthedocs.io.
* Other links: 
        https://go.ncsu.edu/pyswolf

        https://jwlevis.wixsite.com/swolf


Features
--------

* Life cycle assessment of Municipal Solid Waste (MSW) systems. Process models include Landfill, Waste-to-Energy (WTE), Composting, Anaerobic Digestion (AD), Single Stream Material Recovery Facility (MRF), and Collection.
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

        conda create --name PySWOLF python=3.7

5- Activate the environment::

        conda activate PySWOLF

6- Install PySWOLF in the environment::

        pip install PySWOLF

7- Open python to tun PySWOLF::

        ipython

8- Run PySWOLF in python::

        from PySWOLF import *
        PySWOLF()

.. endInstallation
Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
