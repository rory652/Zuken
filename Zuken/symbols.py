from .e3 import Job

_symbol = Job.CreateSymbolObject()
_ = None

def placeSymbol(name: str, version, sheet: int, x: float, y: float) -> int:
    _symbol.Load(name, version)
    # I personally don't have any need for the rotation/scale optional parameters
    return _symbol.Place(sheet, x, y)

def extractSymbolText(symbol: int, category=0, text="") -> list:
    _symbol.SetId(symbol)
    return list(_symbol.GetTextIds(_, category, text)[1][1:])
