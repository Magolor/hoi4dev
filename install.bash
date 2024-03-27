# On MacOS
# Please run:
# brew install freetype imagemagick
export MAGICK_HOME=/opt/homebrew/opt/imagemagick
export PATH=$MAGICK_HOME/bin:$PATH

# On Windows, please checkout:
# https://docs.wand-py.org/en/0.6.12/guide/install.html#install-imagemagick-on-windows
# Then run, for example:
# export MAGICK_HOME=C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI
# export PATH=%MAGICK_HOME%\\bin;%PATH%

export PDOC_ALLOW_EXEC=1
pip install -q -r requirements.txt
pip install -e .

pdoc -d google --output-dir doc hoi4dev

python -c "from hoi4dev import init_config; init_config()"
python -c "import hoi4dev; from pyheaven import GREEN; print(GREEN(f'hoi4dev version {hoi4dev.__version__} successfully installed!'))"
