from .e3 import job as _job

_sheet = _job.CreateSheetObject()
_ = None

def active():
    """
    Returns:
        Active Sheet ID
    """
    return _job.GetActiveSheetId()
