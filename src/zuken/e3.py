# More reliable way of making a COM connection to Zuken
# Taken from "https://stackoverflow.com/a/69288053" by Pelelter
def dispatch(app_name: str):
    try:
        from win32com import client
        app = client.gencache.EnsureDispatch(app_name)
    except AttributeError:
        # Corner case dependencies.
        import os
        import re
        import sys
        import shutil
        # Remove cache and try again.
        MODULE_LIST = [m.__name__ for m in sys.modules.values()]
        for module in MODULE_LIST:
            if re.match(r'win32com\.gen_py\..+', module):
                del sys.modules[module]
        shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))
        from win32com import client
        app = client.gencache.EnsureDispatch(app_name)
    return app

def print(msg, popup=0, item=0):
    """
    Shorthand for the "PutInfo" method

    Args:
        msg: Message to display (gets converted to string automatically, so anything works)
        popup: Whether to display an additional dialogue or not
        item: ID of an item in the project (allows you to jump to it)
    """
    E3.PutInfo(popup, msg, item)

def warn(msg, popup=0, item=0):
    """
    Shorthand for the "PutWarning" method

    Args:
        msg: Message to display (gets converted to string automatically, so anything works)
        popup: Whether to display an additional dialogue or not
        item: ID of an item in the project (allows you to jump to it)
    """
    E3.PutWarning(popup, msg, item)

def error(msg, popup=0, item=0):
    """
    Shorthand for the "PutError" method

    Args:
        msg: Message to display (gets converted to string automatically, so anything works)
        popup: Whether to display an additional dialogue or not
        item: ID of an item in the project (allows you to jump to it)
    """
    E3.PutError(popup, msg, item)

def message(msg, item=0):
    """
    Shorthand for the "PutMessage" method

    Args:
        msg: Message to display (gets converted to string automatically, so anything works)
        item: ID of an item in the project (allows you to jump to it)
    """
    E3.PutMessage(msg, item)

def verify(msg, popup=0, item=0):
    """
    Shorthand for the "PutVerify" method

    Args:
        msg: Message to display (gets converted to string automatically, so anything works)
        popup: Whether to display an additional dialogue or not
        item: ID of an item in the project (allows you to jump to it)
    """
    E3.PutVerify(popup, msg, item)

E3 = dispatch("CT.Application")
"""E3 Object - Links to all instances of the application"""

Job = E3.CreateJobObject()
"""E3 Job Object - Links to a single instance of the application"""


