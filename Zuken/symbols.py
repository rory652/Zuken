from .e3 import Job

_symbol = Job.CreateSymbolObject()
_ = None

def placeSymbol(name: str, version, sheet: int, x: float, y: float) -> int:
    """
    Places specified symbol on the sheet

    Args:
        name: Symbol Name
        version: Symbol Version
        sheet: Sheet to place on
        x: x coordinate
        y: y coordinate

    Returns:
        ID of the new symbol (0 if not created)
    """

    _symbol.Load(name, version)
    # I personally don't have any need for the rotation/scale optional parameters
    return _symbol.Place(sheet, x, y)

def extractSymbolText(symbol: int, category=0, text="") -> list:
    """
    Returns the text IDs from a symbol. Able to filter by category (text type) and text content

    Args:
        symbol: Symbol ID to get text from
        category: Text type to filter the text IDs to. Can be found in Database Editor -> Format -> Text Types
        text: Text string to search for (must be an exact match)

    Returns:
        List of text IDs, will be empty if none are found
    """

    _symbol.SetId(symbol)
    return list(_symbol.GetTextIds(_, category, text)[1][1:])
