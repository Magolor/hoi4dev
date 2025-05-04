from ..base import *
def install_wand():
    """
    Install the Wand library for image processing.
    """
    if is_macos():
        try:
            cmd("brew update & brew upgrade & brew install freetype imagemagick")
        except Exception as e:
            printerr(f"💥 Failed to install ImageMagick: {str(e)}.")
            printerr(f"ImageMagick is a necessary dependency for the Wand library (used for handling images).")
            printerr(f"Please install it manually using the following command.")
            printerr(f"\tbrew install freetype imagemagick")
            raise
        return
    if is_windows():
        try:
            cmd("choco install imagemagick")
        except Exception as e:
            printerr(f"💥 Failed to install ImageMagick: {str(e)}.")
            printerr(f"ImageMagick is a necessary dependency for the Wand library (used for handling images).")
            printerr(f"Please install it manually using the following command.")
            printerr(f"\tchoco install imagemagick")
            raise
        return
    if is_linux():
        raise NotImplementedError("Linux is not supported yet.")

def setup_wand():
    if is_macos():
        os.environ['MAGICK_HOME'] = "/opt/homebrew/opt/imagemagick"
        os.environ['DYLD_LIBRARY_PATH'] = f"{os.environ['MAGICK_HOME']}/lib/"
        os.environ['PATH'] = f"{os.environ['MAGICK_HOME']}/bin:{os.environ['PATH']}"
    if is_windows():
        os.environ['MAGICK_HOME'] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI"
        os.environ['DYLD_LIBRARY_PATH'] = f"{os.environ['MAGICK_HOME']}/lib/"
        os.environ['PATH'] = os.environ['MAGICK_HOME']+"\\bin;"+os.environ['PATH']
    if is_linux():
        raise NotImplementedError("Linux is not supported yet.")
setup_wand()

from .base import *
