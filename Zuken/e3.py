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
    E3.PutInfo(popup, msg, item)

def warn(msg, popup=0, item=0):
    E3.PutWarning(popup, msg, item)

def error(msg, popup=0, item=0):
    E3.PutError(popup, msg, item)

def message(msg, item=0):
    E3.PutMessage(msg, item)

def verify(msg, popup=0, item=0):
    E3.PutVerify(popup, msg, item)

E3 = dispatch("CT.Application")
Job = E3.CreateJobObject()


