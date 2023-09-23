import setuptools
from pathlib import Path

long_description = Path('README.md').read_text()
requirements = Path('requirements.txt').read_text().splitlines()
# pip install termcolor rich tabulate charset-normalizer
# test: pip install termcolor rich tabulate charset-normalizer pytest

setuptools.setup(
    name='sets-matcher',
    version='0.1.3',
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
