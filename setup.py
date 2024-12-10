from setuptools import setup, find_packages
import pkg_resources

import pathlib
here = pathlib.Path(__file__).parent.resolve()
version = '0.1.0.7'
short_description = "HOI4DEV: Hearts of Iron IV Development Tools"
long_description = (here/"README.md").read_text(encoding="utf-8")
install_requires = [
    'click~=8.1.7',
    'jsonlines~=4.0.0',
    'numpy<2.0.0,>=1.26.4',
    'openai~=1.57.1',
    'pandas~=2.0.3',
    'pdoc~=15.0.0',
    'pillow~=10.3.0',
    'pyheaven>=0.1.6.5',
    'send2trash~=1.8.0',
    'Wand~=0.6.13'
]

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
    install_requires=install_requires,
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
