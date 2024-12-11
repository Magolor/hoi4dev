# On MacOS
# brew install freetype imagemagick
export MAGICK_HOME=/opt/homebrew/opt/imagemagick
export PATH=$MAGICK_HOME/bin:$PATH

export PDOC_ALLOW_EXEC=1
python -m pip install -q -r requirements.txt
python -m pip install -e .

pdoc -d google --output-dir doc hoi4dev

hoi4dev init
hoi4dev -v