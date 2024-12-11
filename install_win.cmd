@echo off
REM Set the MAGICK_HOME environment variable
set "MAGICK_HOME=C:\Program Files\ImageMagick-7.1.1-Q16-HDRI"

REM Add ImageMagick's bin directory to the PATH
set "PATH=%MAGICK_HOME%\bin;%PATH%"

REM Set PDOC_ALLOW_EXEC environment variable
set "PDOC_ALLOW_EXEC=1"

python -m pip install -q -r requirements.txt
python -m pip install -e .

REM Run pdoc to generate documentation in Google style
pdoc -d google --output-dir doc hoi4dev

hoi4dev init
hoi4dev -v