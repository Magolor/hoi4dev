@echo off
REM Set the MAGICK_HOME environment variable
set "MAGICK_HOME=C:\Program Files\ImageMagick-7.1.0-Q16-HDRI"

REM Add ImageMagick's bin directory to the PATH
set "PATH=%MAGICK_HOME%\bin;%PATH%"

REM Set PDOC_ALLOW_EXEC environment variable
set "PDOC_ALLOW_EXEC=1"

pip install -e .

REM Run pdoc to generate documentation in Google style
pdoc -d google --output-dir doc hoi4dev

REM Initialize configuration for hoi4dev
python -c "from hoi4dev import init_config; init_config()"

REM Check the version of hoi4dev and confirm successful installation
python -c "import hoi4dev & echo hoi4dev version %hoi4dev.__version% successfully installed!"