# On Windows
# Download and Install Imagemagick from https://imagemagick.org/archive/binaries/ImageMagick-7.1.1-41-Q16-HDRI-x64-dll.exe
export MAGICK_HOME="C:\Program Files\ImageMagick-7.1.1-Q16-HDRI"
export PATH=$MAGICK_HOME/bin:$PATH

export PDOC_ALLOW_EXEC=1
python -m pip install -q -r requirements.txt
python -m pip install -e .

pdoc -d google --output-dir doc hoi4dev

hoi4dev init
hoi4dev -v