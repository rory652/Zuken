from .e3 import Job
from re import sub

_device = Job.CreateDeviceObject()
_ = None

def devicesOnSheet(sheet: int, base=False) -> list:
    """
    Gets Device IDs for all the devices found on the sheet.
    Found by going through each symbol and seeing if it connects to a Device.

    Args:
        sheet: Sheet to search through
        base: Boolean (default False) to decide whether to return Sheet ID or base (Schematic) ID

    Returns:
        List of device IDs
    """

    Sheet = Job.CreateSheetObject()
    Sheet.SetId(sheet)
    base &= Sheet.IsFormboard()

    devices = []
    for sym in Sheet.GetSymbolIds(_)[1][1:]:
        if (devId := _device.SetId(sym)) == 0:
            continue

        if base:
            devId = _device.GetOriginalId()

        if devId not in devices:
            devices.append(devId)

    return devices

def deviceFormboardId(device: int, sheet: int) -> int:
    """
    Returns the device's ID on a given formboard sheet.
    Given ID can be a formboard ID, even from a different sheet.

    Args:
        device: Device ID to search for
        sheet: Sheet to search for device on

    Returns:
        ID of the device if found, 0 otherwise

    """
    _device.SetId(device)
    if _device.GetFormboardSheetId() == sheet:
        return device

    if _device.IsFormboard():
        _device.SetId(_device.GetOriginalId())

    for d in _device.GetFormboardIds(_)[1][1:]:
        _device.SetId(d)
        if _device.GetFormboardSheetId() == sheet:
            return d
    return 0

def tableSymbolId(device: int, sheet: int) -> int:
    """
    Returns the table symbol for a device on a specific sheet

    Args:
        device: Device ID
        sheet: Sheet ID (should be formboard)

    Returns:
        ID of the table symbol if found, 0 otherwise
    """
    _device.SetId(deviceFormboardId(device, sheet))
    return _device.GetTableSymbolId()

def coreIds(device: int) -> list:
    """
    Gets the core IDs for all wires/cables connected to a device

    Args:
        device: Device ID

    Returns:
        List of cores found connected to the device
    """
    Pin = Job.CreatePinObject()
    _device.SetId(device)

    cores = []
    for p in _device.GetPinIds(_)[1][1:]:
        Pin.SetId(p)
        cores += list(Pin.GetCoreIds(_)[1][1:])
    return cores

def filterByDeviceCode(devices: list, code: str) -> list:
    """
    Filters a list of devices based on the device code, e.g. '-C' for connectors

    Args:
        devices: List of device IDs
        code: Device Letter Code to filter by

    Returns:
        List of devices matching the filter code
    """
    def getCode(device) -> str:
        _device.SetId(device)
        return sub(r"\d", "", _device.GetName())

    return [d for d in devices if getCode(d) == code]

def filterByDeviceAssignment(devices: list, assignment: str) -> list:
    """
    Filters a list of devices based on the device assignment

    Args:
        devices: List of device IDs
        assignment: Device Assignment to filter by

    Returns:
        List of devices matching the filter assignment
    """
    def getAssignment(device) -> str:
        _device.SetId(device)
        return _device.GetAssignment()[1:]

    return [d for d in devices if getAssignment(d) == assignment]

def filterByDeviceLocation(devices: list, location: str) -> list:
    """
    Filters a list of devices based on the device location

    Args:
        devices: List of device IDs
        location: Device loation to filter by

    Returns:
        List of devices matching the filter location
    """

    def getLocation(device) -> str:
        _device.SetId(device)
        return _device.GetLocation()[1:]

    return [d for d in devices if getLocation(d) == location]

def filterByDeviceAttribute(devices: list, attribute: str, value: str, component=False) -> list:
    """
    Filters a list of devices based on the device/component attribute value

    Args:
        devices: List of device IDs
        attribute: Attribute to get value of
        value: Value to compare the attribute again
        component: True to use component attribute, False (default) to use device attribute

    Returns:
        List of devices matching the filter attribute
    """
    def getAttribute(device) -> str:
        _device.SetId(device)

        if component:
            return _device.GetComponentAttributeValue(attribute)
        else:
            return _device.GetAttributeValue(attribute)

    return [d for d in devices if getAttribute(d) == value]

def filterByDeviceClass(devices: list, cls: str) -> list:
    """
    Filters a list of devices based on the device class

    Args:
        devices: List of device IDs
        cls: Class to filter by

    Returns:
        List of devices matching the filter class
    """
    return filterByDeviceAttribute(devices, "Class", cls, True)
