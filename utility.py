# General utility module for the Epidemic application

import os
import platform


def get_path(filename):
    """Return the full path for the passed filename. This works cross-platform
    and uses AppKit to refer to the path when used on macOS.
    This uses code suggested on this pyinstaller issues page:
    https://github.com/pyinstaller/pyinstaller/issues/5109#issuecomment-683313824"""
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    if platform.system() == "Darwin":
        from AppKit import NSBundle
        file = NSBundle.mainBundle().pathForResource_ofType_(name, ext)
        return file or os.path.realpath(filename)
    else:
        return os.path.realpath(filename)