import setuptools
from pathlib import Path

long_description = Path('README.md').read_text()
requirements = Path('requirements.txt').read_text().splitlines()
# pip install rich tabulate charset-normalizer
# test: pip install rich tabulate charset-normalizer pytest mypy

version_path = Path(__file__).parent / "sets_matcher/__version__.py"
version_info = {}
exec(version_path.read_text(), version_info)

setuptools.setup(
    name='sets-matcher',
    version=version_info["__version__"],
    author="streanger",
    description="sets matcher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/streanger/sets-matcher",
    packages=['sets_matcher',],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "matcher=sets_matcher:main",
        ]
    },
)
