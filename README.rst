#########
whey-pth
#########

.. start short_desc

**Extension to whey to support .pth files.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/whey-pth/latest?logo=read-the-docs
	:target: https://whey-pth.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/repo-helper/whey-pth/workflows/Docs%20Check/badge.svg
	:target: https://github.com/repo-helper/whey-pth/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/repo-helper/whey-pth/workflows/Linux/badge.svg
	:target: https://github.com/repo-helper/whey-pth/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/repo-helper/whey-pth/workflows/Windows/badge.svg
	:target: https://github.com/repo-helper/whey-pth/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/repo-helper/whey-pth/workflows/macOS/badge.svg
	:target: https://github.com/repo-helper/whey-pth/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/repo-helper/whey-pth/workflows/Flake8/badge.svg
	:target: https://github.com/repo-helper/whey-pth/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/repo-helper/whey-pth/workflows/mypy/badge.svg
	:target: https://github.com/repo-helper/whey-pth/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/repo-helper/whey-pth/requirements.svg?branch=master
	:target: https://requires.io/github/repo-helper/whey-pth/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/repo-helper/whey-pth/master?logo=coveralls
	:target: https://coveralls.io/github/repo-helper/whey-pth?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/repo-helper/whey-pth?logo=codefactor
	:target: https://www.codefactor.io/repository/github/repo-helper/whey-pth
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/whey-pth
	:target: https://pypi.org/project/whey-pth/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/whey-pth?logo=python&logoColor=white
	:target: https://pypi.org/project/whey-pth/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/whey-pth
	:target: https://pypi.org/project/whey-pth/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/whey-pth
	:target: https://pypi.org/project/whey-pth/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/whey-pth?logo=anaconda
	:target: https://anaconda.org/domdfcoding/whey-pth
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/whey-pth?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/whey-pth
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/repo-helper/whey-pth
	:target: https://github.com/repo-helper/whey-pth/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/repo-helper/whey-pth
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/repo-helper/whey-pth/v0.0.0
	:target: https://github.com/repo-helper/whey-pth/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/repo-helper/whey-pth
	:target: https://github.com/repo-helper/whey-pth/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/whey-pth
	:target: https://pypi.org/project/whey-pth/
	:alt: PyPI - Downloads

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/repo-helper/whey-pth/master.svg
	:target: https://results.pre-commit.ci/latest/github/repo-helper/whey-pth/master
	:alt: pre-commit.ci status

.. end shields

Installation
--------------

.. start installation

``whey-pth`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install whey-pth

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels http://conda.anaconda.org/conda-forge
		$ conda config --add channels http://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install whey-pth

.. end installation
