# stdlib
import tarfile
import tempfile
import zipfile

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture, check_file_regression
from domdf_python_tools.paths import PathPlus
from pytest_regressions.file_regression import FileRegressionFixture
from whey.builder import SDistBuilder
from whey.config import BadConfigError, load_toml
from whey.foreman import Foreman

# this package
from whey_pth import PthWheelBuilder, WheyPthParser

WHEY_NO_PTH = """\
[build-system]
requires = [ "whey",]
build-backend = "whey"

[project]
name = "whey"
version = "2021.0.0"
description = "A simple Python wheel builder for simple projects."
keywords = [ "pep517", "pep621", "build", "sdist", "wheel", "packaging", "distribution",]
dynamic = [ "classifiers", "requires-python",]
readme = "README.rst"
dependencies = [
  "httpx",
  "gidgethub[httpx]>4.0.0",
  "django>2.1; os_name != 'nt'",
  "django>2.0; os_name == 'nt'"
]

[project.license]
file = "LICENSE"

[[project.authors]]
email = "dominic@davis-foster.co.uk"
name = "Dominic Davis-Foster"

[project.urls]
Homepage = "https://whey.readthedocs.io/en/latest"
Documentation = "https://whey.readthedocs.io/en/latest"
"Issue Tracker" = "https://github.com/repo-helper/whey/issues"
"Source Code" = "https://github.com/repo-helper/whey"

[tool.whey]
base-classifiers = [ "Development Status :: 4 - Beta",]
python-versions = [ "3.6", "3.7", "3.8", "3.9", "3.10",]
python-implementations = [ "CPython", "PyPy",]
platforms = [ "Windows", "macOS", "Linux",]
license-key = "MIT"

[tool.whey.builders]
wheel = "whey_pth_wheel"
"""

COMPLETE_A = """\
[build-system]
requires = [ "whey",]
build-backend = "whey"

[project]
name = "whey"
version = "2021.0.0"
description = "A simple Python wheel builder for simple projects."
keywords = [ "pep517", "pep621", "build", "sdist", "wheel", "packaging", "distribution",]
dynamic = [ "classifiers", "requires-python",]
readme = "README.rst"
dependencies = [
  "httpx",
  "gidgethub[httpx]>4.0.0",
  "django>2.1; os_name != 'nt'",
  "django>2.0; os_name == 'nt'"
]

[project.license]
file = "LICENSE"

[[project.authors]]
email = "dominic@davis-foster.co.uk"
name = "Dominic Davis-Foster"

[project.urls]
Homepage = "https://whey.readthedocs.io/en/latest"
Documentation = "https://whey.readthedocs.io/en/latest"
"Issue Tracker" = "https://github.com/repo-helper/whey/issues"
"Source Code" = "https://github.com/repo-helper/whey"

[tool.whey]
base-classifiers = [ "Development Status :: 4 - Beta",]
python-versions = [ "3.6", "3.7", "3.8", "3.9", "3.10",]
python-implementations = [ "CPython", "PyPy",]
platforms = [ "Windows", "macOS", "Linux",]
license-key = "MIT"

[tool.whey.builders]
wheel = "whey_pth_wheel"

[tool.whey-pth]
name = "my_project.pth"
pth-content = "import _virtualenv"
"""

COMPLETE_B = """\
[build-system]
requires = [ "whey",]
build-backend = "whey"

[project]
name = "whey"
version = "2021.0.0"
description = "A simple Python wheel builder for simple projects."
keywords = [ "pep517", "pep621", "build", "sdist", "wheel", "packaging", "distribution",]
dynamic = [ "classifiers", "requires-python",]
readme = "README.rst"
dependencies = [
  "httpx",
  "gidgethub[httpx]>4.0.0",
  "django>2.1; os_name != 'nt'",
  "django>2.0; os_name == 'nt'"
]

[project.license]
file = "LICENSE"

[[project.authors]]
email = "dominic@davis-foster.co.uk"
name = "Dominic Davis-Foster"

[project.urls]
Homepage = "https://whey.readthedocs.io/en/latest"
Documentation = "https://whey.readthedocs.io/en/latest"
"Issue Tracker" = "https://github.com/repo-helper/whey/issues"
"Source Code" = "https://github.com/repo-helper/whey"

[tool.whey]
base-classifiers = [ "Development Status :: 4 - Beta",]
python-versions = [ "3.6", "3.7", "3.8", "3.9", "3.10",]
python-implementations = [ "CPython", "PyPy",]
platforms = [ "Windows", "macOS", "Linux",]
license-key = "MIT"

[tool.whey.builders]
wheel = "whey_pth_wheel"

[tool.whey-pth]
name = "my_project"
pth-content = "import _virtualenv"
"""


@pytest.mark.parametrize(
		"config",
		[
				pytest.param(WHEY_NO_PTH, id="WHEY_NO_PTH"),
				pytest.param(COMPLETE_A, id="COMPLETE_A"),
				pytest.param(COMPLETE_B, id="COMPLETE_B"),
				],
		)
def test_build_complete(
		config: str,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		file_regression: FileRegressionFixture,
		capsys,
		):
	(tmp_pathplus / "pyproject.toml").write_clean(config)
	(tmp_pathplus / "whey").mkdir()
	(tmp_pathplus / "whey" / "__init__.py").write_clean("print('hello world)")
	(tmp_pathplus / "README.rst").write_clean("Spam Spam Spam Spam")
	(tmp_pathplus / "LICENSE").write_clean("This is the license")
	(tmp_pathplus / "requirements.txt").write_clean("domdf_python_tools")

	data = {}

	with tempfile.TemporaryDirectory() as tmpdir:
		wheel_builder = PthWheelBuilder(
				project_dir=tmp_pathplus,
				config=load_toml(tmp_pathplus / "pyproject.toml"),
				build_dir=tmpdir,
				out_dir=tmp_pathplus,
				verbose=True,
				colour=False,
				)
		wheel = wheel_builder.build_wheel()
		assert (tmp_pathplus / wheel).is_file()
		zip_file = zipfile.ZipFile(tmp_pathplus / wheel)
		data["wheel_content"] = sorted(zip_file.namelist())

		with zip_file.open("whey/__init__.py", mode='r') as fp:
			assert fp.read().decode("UTF-8") == "print('hello world)\n"

		with zip_file.open("whey-2021.0.0.dist-info/METADATA", mode='r') as fp:
			check_file_regression(fp.read().decode("UTF-8"), file_regression)

		if config != WHEY_NO_PTH:
			with zip_file.open("my_project.pth", mode='r') as fp:
				assert fp.read().decode("UTF-8") == "import _virtualenv\n"

	with tempfile.TemporaryDirectory() as tmpdir:
		sdist_builder = SDistBuilder(
				project_dir=tmp_pathplus,
				config=load_toml(tmp_pathplus / "pyproject.toml"),
				build_dir=tmpdir,
				out_dir=tmp_pathplus,
				verbose=True,
				colour=False,
				)
		sdist = sdist_builder.build_sdist()
		assert (tmp_pathplus / sdist).is_file()

		tar = tarfile.open(tmp_pathplus / sdist)
		data["sdist_content"] = sorted(tar.getnames())

		with tar.extractfile("whey-2021.0.0/whey/__init__.py") as fp:  # type: ignore
			assert fp.read().decode("UTF-8") == "print('hello world)\n"
		with tar.extractfile("whey-2021.0.0/README.rst") as fp:  # type: ignore
			assert fp.read().decode("UTF-8") == "Spam Spam Spam Spam\n"
		with tar.extractfile("whey-2021.0.0/LICENSE") as fp:  # type: ignore
			assert fp.read().decode("UTF-8") == "This is the license\n"
		with tar.extractfile("whey-2021.0.0/requirements.txt") as fp:  # type: ignore
			assert fp.read().decode("UTF-8") == "domdf_python_tools\n"

	outerr = capsys.readouterr()
	data["stdout"] = outerr.out.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = outerr.err

	advanced_data_regression.check(data)


@pytest.mark.parametrize(
		"config",
		[
				pytest.param(WHEY_NO_PTH, id="WHEY_NO_PTH"),
				pytest.param(COMPLETE_A, id="COMPLETE_A"),
				pytest.param(COMPLETE_B, id="COMPLETE_B"),
				],
		)
def test_build_complete_foreman(
		config: str,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		file_regression: FileRegressionFixture,
		capsys,
		):
	(tmp_pathplus / "pyproject.toml").write_clean(config)
	(tmp_pathplus / "whey").mkdir()
	(tmp_pathplus / "whey" / "__init__.py").write_clean("print('hello world)")
	(tmp_pathplus / "README.rst").write_clean("Spam Spam Spam Spam")
	(tmp_pathplus / "LICENSE").write_clean("This is the license")
	(tmp_pathplus / "requirements.txt").write_clean("domdf_python_tools")

	data = {}

	foreman = Foreman(project_dir=tmp_pathplus)

	with tempfile.TemporaryDirectory() as tmpdir:
		wheel = foreman.build_wheel(
				build_dir=tmpdir,
				out_dir=tmp_pathplus,
				verbose=True,
				colour=False,
				)

		assert (tmp_pathplus / wheel).is_file()
		zip_file = zipfile.ZipFile(tmp_pathplus / wheel)
		data["wheel_content"] = sorted(zip_file.namelist())

		with zip_file.open("whey/__init__.py", mode='r') as fp:
			assert fp.read().decode("UTF-8") == "print('hello world)\n"

		with zip_file.open("whey-2021.0.0.dist-info/METADATA", mode='r') as fp:
			check_file_regression(fp.read().decode("UTF-8"), file_regression)

		if config != WHEY_NO_PTH:
			with zip_file.open("my_project.pth", mode='r') as fp:
				assert fp.read().decode("UTF-8") == "import _virtualenv\n"

	with tempfile.TemporaryDirectory() as tmpdir:
		sdist = foreman.build_sdist(
				build_dir=tmpdir,
				out_dir=tmp_pathplus,
				verbose=True,
				colour=False,
				)
		assert (tmp_pathplus / sdist).is_file()

		tar = tarfile.open(tmp_pathplus / sdist)
		data["sdist_content"] = sorted(tar.getnames())

		with tar.extractfile("whey-2021.0.0/whey/__init__.py") as fp:  # type: ignore
			assert fp.read().decode("UTF-8") == "print('hello world)\n"
		with tar.extractfile("whey-2021.0.0/README.rst") as fp:  # type: ignore
			assert fp.read().decode("UTF-8") == "Spam Spam Spam Spam\n"
		with tar.extractfile("whey-2021.0.0/LICENSE") as fp:  # type: ignore
			assert fp.read().decode("UTF-8") == "This is the license\n"
		with tar.extractfile("whey-2021.0.0/requirements.txt") as fp:  # type: ignore
			assert fp.read().decode("UTF-8") == "domdf_python_tools\n"

	outerr = capsys.readouterr()
	data["stdout"] = outerr.out.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = outerr.err

	advanced_data_regression.check(data)


def test_build_additional_files(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		file_regression: FileRegressionFixture,
		capsys,
		):

	(tmp_pathplus / "pyproject.toml").write_lines([
			COMPLETE_A,
			'',
			"additional-wheel-files = [",
			'  "include _virtualenv.py",',
			']',
			])
	(tmp_pathplus / "whey").mkdir()
	(tmp_pathplus / "whey" / "__init__.py").write_clean("print('hello world)")
	(tmp_pathplus / "_virtualenv.py").write_clean("This is the _virtualenv.py file")
	(tmp_pathplus / "README.rst").write_clean("Spam Spam Spam Spam")
	(tmp_pathplus / "LICENSE").write_clean("This is the license")
	(tmp_pathplus / "requirements.txt").write_clean("domdf_python_tools")

	data = {}

	with tempfile.TemporaryDirectory() as tmpdir:
		wheel_builder = PthWheelBuilder(
				project_dir=tmp_pathplus,
				config=load_toml(tmp_pathplus / "pyproject.toml"),
				build_dir=tmpdir,
				out_dir=tmp_pathplus,
				verbose=True,
				colour=False,
				)
		wheel = wheel_builder.build_wheel()
		assert (tmp_pathplus / wheel).is_file()
		zip_file = zipfile.ZipFile(tmp_pathplus / wheel)
		data["wheel_content"] = sorted(zip_file.namelist())

		with zip_file.open("whey/__init__.py", mode='r') as fp:
			assert fp.read().decode("UTF-8") == "print('hello world)\n"

		with zip_file.open("whey-2021.0.0.dist-info/METADATA", mode='r') as fp:
			check_file_regression(fp.read().decode("UTF-8"), file_regression)

		with zip_file.open("my_project.pth", mode='r') as fp:
			assert fp.read().decode("UTF-8") == "import _virtualenv\n"

		with zip_file.open("_virtualenv.py", mode='r') as fp:
			assert fp.read().decode("UTF-8") == "This is the _virtualenv.py file\n"

	outerr = capsys.readouterr()
	data["stdout"] = outerr.out.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = outerr.err

	advanced_data_regression.check(data)


def test_badconfig():
	with pytest.raises(BadConfigError, match=r"The \[tool.whey-pth.name\] key is required."):
		WheyPthParser().parse({})

	with pytest.raises(BadConfigError, match=r"The \[tool.whey-pth.name\] key is required."):
		WheyPthParser().parse({"pth-content": "import _virtualenv"})

	with pytest.raises(BadConfigError, match=r"The \[tool.whey-pth.pth-content\] key is required."):
		WheyPthParser().parse({"name": "foo"})


def test_badconfig_set_defaults():
	with pytest.raises(BadConfigError, match=r"The \[tool.whey-pth.name\] key is required."):
		WheyPthParser().parse({}, set_defaults=True)

	with pytest.raises(BadConfigError, match=r"The \[tool.whey-pth.name\] key is required."):
		WheyPthParser().parse({"pth-content": "import _virtualenv"}, set_defaults=True)

	with pytest.raises(BadConfigError, match=r"The \[tool.whey-pth.pth-content\] key is required."):
		WheyPthParser().parse({"name": "foo"}, set_defaults=True)
