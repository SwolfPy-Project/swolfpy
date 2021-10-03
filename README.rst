.. General

================================================================
Solid Waste Optimization Life-cycle Framework in Python(SwolfPy)
================================================================

.. image:: https://img.shields.io/pypi/v/swolfpy.svg
        :target: https://pypi.python.org/pypi/swolfpy
        
.. image:: https://img.shields.io/pypi/pyversions/swolfpy.svg
    :target: https://pypi.org/project/swolfpy/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/swolfpy.svg
    :target: https://pypi.org/project/swolfpy/
    :alt: License

.. image:: https://img.shields.io/pypi/dm/swolfpy.svg?label=Pypi%20downloads
    :target: https://pypi.org/project/swolfpy/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/format/swolfpy.svg
    :target: https://pypi.org/project/swolfpy/
    :alt: Format

.. image:: https://readthedocs.org/projects/swolfpy/badge/?version=latest
        :target: https://swolfpy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://github.com/SwolfPy-Project/swolfpy/actions/workflows/python-app.yml/badge.svg?branch=master
        :target: https://github.com/SwolfPy-Project/swolfpy/actions/workflows/python-app.yml
        :alt: Test

.. image:: https://zenodo.org/badge/395802952.svg
        :target: https://zenodo.org/badge/latestdoi/395802952
        :alt: DOi


* Free software: GNU GENERAL PUBLIC LICENSE V2
* Documentation: https://swolfpy.readthedocs.io.
* Repository: https://github.com/SwolfPy-Project/swolfpy
* Other links: 

  * https://go.ncsu.edu/swolfpy
  * https://jwlevis.wixsite.com/swolf


Features
--------

* **Life-cycle assessment of Municipal Solid Waste (MSW) systems**

  * Comparative LCA
  * Contribution analysis
  * LCI report

* **Monte Carlo simulation**

  * Uncertainty analysis
  * Data visualization (distributions & correlations)

* **Optimization**

  * Minimize environmental burdens or cost subject to a number of technical or policy-related constraints


.. list-table:: **Life-cycle process models**
   :widths: auto
   :header-rows: 1

   * - 
     - Process model 
     - Description
   * - 1
     - Landfill (**LF**)
     - Calculates emissions, material use, and energy use associated with construction, operations, 
       closure and post-closure activities, landfill gas and leachate management, and carbon storage.
   * - 2
     - Waste-to-Energy (**WTE**)
     - Calculates emissions, mass flows, and resource use and recovery for the mass burn WTE process.
   * - 3
     - Gasification & Syngas Combustion (**GC**)
     - Calculates emissions, mass flows, and resource use and recovery for the GC process (Produced syngas from
       gasification is combusted to produce electricity by steam turbine). 
   * - 4
     - Composting (**Comp**)
     - Calculates emissions, mass flows, and resource use and recovery for aerobic composting process and final use of compost.
   * - 5
     - Home Composting (**HC**)
     - Calculates emissions, mass flows, and resource use and recovery for home composting process and final use of compost.
   * - 6
     - Anaerobic Digestion (**AD**)
     - Calculates emissions, mass flows, and resource use and recovery for anaerobic digestion process and final use of compost.
   * - 7
     - Single-Stream Material Recovery facility (**SS_MRF**)
     - Calculates cost, emissions, and energy use associated with material recovery facilities.
   * - 8
     - Refuse-Derived Fuel (**RDF**)
     - Calculates cost, emissions, and energy use associated with RDF prodcution facilities.
   * - 9
     - Reprocessing (**Reproc**)
     - Calculates emissions, mass flows, and resource use and recovery associated with recycling materials.	 
   * - 10
     - Transfer Station (**TS**)
     - Calculates cost, emissions, and energy use associated with Transfer Stations.
   * - 11
     - Single Family Collection (**SF_Col**)
     - Calculates cost, emissions, and fossil fuel use associated with MSW collection.


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

4- Create a new environment for swolfpy::

        conda create --name swolfpy python=3.7

5- Activate the environment::

        conda activate swolfpy

6- Install swolfpy in the environment::

        pip install swolfpy

7- Open python to run swolfpy::

        python

8- Run swolfpy in python::

        import swolfpy as sp 
        sp.swolfpy()

.. endInstallation
