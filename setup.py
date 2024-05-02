from setuptools import setup, find_namespace_packages, SetuptoolsDeprecationWarning
import pkg_resources
import warnings
warnings.filterwarnings('ignore', category=SetuptoolsDeprecationWarning)

with open("README.md", "r") as fh:
    long_description = fh.read()

from __init__ import __version__
from pyheaven import BLUE
print(BLUE(f"Installing HOI4DEV version: {__version__}."))
setup(
    name = "hoi4dev",
    version = __version__,
    author = "Magolor",
    author_email = "magolorcz@gmail.com",
    description = "HOI4DEV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/Magolor/",
    project_urls={
        "Author":"https://github.com/Magolor/",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir={"":"src"},
    packages=find_namespace_packages(where="src"),
    package_data={
        'hoi4dev': ['resources/**/*'],
    },
    python_requires=">=3.9",
)
