=====================
Configuration
=====================

``whey-pth`` is configured in the ``pyproject.toml`` file defined in :pep:`517` and :pep:`518`.

.. seealso::

	The `whey documentation <https://whey.readthedocs.io/en/latest/configuration.html>`_
	contains instructions for configuring ``whey`` itself.

To enable ``whey-pth``, add the following lines to your ``pyprojet.toml`` file:

.. code-block:: TOML

	[tool.whey.builders]
	wheel = "whey_pth_wheel"

The ``whey-pth``-specific configuration is defined in the ``tool.whey-pth`` table.


``[tool.whey-pth]``
-------------------

As a minimum, this table should contain the keys :conf:`name` and :conf:`pth-content`.


.. conf:: name

	**Type**: :toml:`String`

	The filename of the ``.pth`` file, relative to the root of the distribution archive.
	If the filename does not end with ``.pth`` the extension will be appended automatically.

	:bold-title:`Example:`

	.. code-block:: TOML

		[tool.whey-pth]
		name = "virtualenv.pth"

.. conf:: pth-content

	**Type**: :toml:`String`

	The content of the ``.pth`` file. See https://docs.python.org/3/library/site.html for details on the expected contents of the file.

	:bold-title:`Example:`

	.. code-block:: TOML

		[tool.whey-pth]
		pth-content = "import _virtualenv"


.. conf:: additional-wheel-files

	**Type**: :toml:`Array` of :toml:`strings <String>`

	A list of `MANIFEST.in <https://packaging.python.org/guides/using-manifest-in/>`_-style
	entries for additional files to include in the wheel.

	The supported commands are:

	=========================================================  ==================================================================================================
	Command                                                    Description
	=========================================================  ==================================================================================================
	:samp:`include {pat1} {pat2} ...`                          Add all files matching any of the listed patterns
	:samp:`exclude {pat1} {pat2} ...`                          Remove all files matching any of the listed patterns
	:samp:`recursive-include {dir-pattern} {pat1} {pat2} ...`  Add all files under directories matching ``dir-pattern`` that match any of the listed patterns
	:samp:`recursive-exclude {dir-pattern} {pat1} {pat2} ...`  Remove all files under directories matching ``dir-pattern`` that match any of the listed patterns
	=========================================================  ==================================================================================================

	.. TODO:: example
