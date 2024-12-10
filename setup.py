from setuptools import setup, find_packages

import pathlib
here = pathlib.Path(__file__).parent.resolve()
version = '0.1.0.4'
short_description = "HOI4DEV: Hearts of Iron IV Development Tools"
long_description = (here / "README.md").read_text(encoding="utf-8")

print(f"Installing HOI4DEV version: {version}.")
setup(
    name = "hoi4dev",
    version = version,
    author = "Magolor",
    author_email = "magolorcz@gmail.com",
    description = short_description,
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/Magolor/",
    project_urls={
        "Author":"https://github.com/Magolor/",
    },
    python_requires=">=3.9, <4",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    entry_points = '''
        [console_scripts]
        hoi4dev=hoi4dev.cli:cli
    ''',
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={
        'hoi4dev': ['resources/**/*'],
    }
)
