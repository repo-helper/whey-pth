#!/usr/bin/env python3
#
#  __init__.py
"""
Extension to whey to support .pth files.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Dict, List

# 3rd party
import dom_toml
from dom_toml.parser import TOML_TYPES, AbstractConfigParser, BadConfigError
from whey.builder import WheelBuilder

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.3"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["PthWheelBuilder", "WheyPthParser"]


class PthWheelBuilder(WheelBuilder):
	"""
	Builds wheel binary distributions using metadata read from ``pyproject.toml``.

	This builder has added support for creating ``.pth`` files.

	:param project_dir: The project to build the distribution for.
	:param build_dir: The (temporary) build directory.
	:default build_dir: :file:`{<project_dir>}/build/wheel`
	:param out_dir: The output directory.
	:default out_dir: :file:`{<project_dir>}/dist`
	:param verbose: Enable verbose output.
	"""

	def write_pth_files(self):
		"""
		Write ``.pth`` files, and their associated files, into the build directory.
		"""

		config = dom_toml.load(self.project_dir / "pyproject.toml")

		if "whey-pth" not in config.get("tool", {}):
			return

		parsed_config = WheyPthParser().parse(config["tool"]["whey-pth"], set_defaults=True)

		pth_filename = self.build_dir / parsed_config["name"]

		if not pth_filename.suffix == ".pth":
			pth_filename = pth_filename.with_suffix(".pth")

		pth_filename.write_clean(parsed_config["pth-content"])
		self.report_written(pth_filename)

		self.parse_additional_files(*parsed_config["additional-wheel-files"])

	call_additional_hooks = write_pth_files


class WheyPthParser(AbstractConfigParser):
	"""
	Parser for the ``[tool.whey-pth]`` table from ``pyproject.toml``.
	"""

	factories = {"additional-wheel-files": list}

	def parse_name(self, config: Dict[str, TOML_TYPES]) -> str:
		"""
		Parse the ``name`` key, giving the desired name of the ``.pth`` file.

		:param config: The unparsed TOML config for the ``[tool.whey-pth]`` table.
		"""

		name = config["name"]

		self.assert_type(name, str, ["tool", "whey-pth", "name"])

		return name

	def parse_pth_content(self, config: Dict[str, TOML_TYPES]) -> str:
		"""
		Parse the ``pth-content`` key, giving the content of the ``.pth`` file.

		:param config: The unparsed TOML config for the ``[tool.whey-pth]`` table.
		"""

		pth_content = config["pth-content"]

		self.assert_type(pth_content, str, ["tool", "whey-pth", "pth-content"])

		return pth_content

	def parse_additional_wheel_files(self, config: Dict[str, TOML_TYPES]) -> List[str]:
		"""
		Parse the ``additional-wheel-files`` key,
		giving `MANIFEST.in <https://packaging.python.org/guides/using-manifest-in/>`_-style
		entries for additional files to include in the wheel.

		:param config: The unparsed TOML config for the ``[tool.whey-pth]`` table.
		"""  # noqa: D400

		additional_files = config["additional-wheel-files"]

		for idx, file in enumerate(additional_files):
			self.assert_indexed_type(file, str, ["tool", "whey", "additional-wheel-files"], idx=idx)

		return additional_files

	@property
	def keys(self) -> List[str]:
		"""
		The keys to parse from the TOML file.
		"""

		return [
				"name",
				"pth-content",
				"additional-wheel-files",
				]

	def parse(
			self,
			config: Dict[str, TOML_TYPES],
			set_defaults: bool = False,
			) -> Dict[str, TOML_TYPES]:
		"""
		Parse the TOML configuration.

		:param config:
		:param set_defaults: If :py:obj:`True`, the values in :attr:`dom_toml.parser.AbstractConfigParser.defaults`
			and :attr:`dom_toml.parser.AbstractConfigParser.factories` will be set as defaults for the returned mapping.
		"""

		if "name" not in config:
			raise BadConfigError("The [tool.whey-pth.name] key is required.")
		if "pth-content" not in config:
			raise BadConfigError("The [tool.whey-pth.pth-content] key is required.")

		parsed_config = super().parse(config, set_defaults=set_defaults)

		return parsed_config
