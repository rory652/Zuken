import re
from .e3 import job as _job

_device = _job.CreateDeviceObject()
_ = None

def onSheet(sheet: int, base=False) -> list:
    """
    Gets Device IDs for all the devices found on the sheet.
    Found by going through each symbol and seeing if it connects to a Device.

    Args:
        sheet: Sheet to search through
        base: Boolean (default False) to decide whether to return Sheet ID or base (Schematic) ID

    Returns:
        List of device IDs
    """

    Sheet = _job.CreateSheetObject()
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

def formboardId(device: int, sheet: int) -> int:
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
    _device.SetId(formboardId(device, sheet))
    return _device.GetTableSymbolId()

def coreIds(device: int, nc=False) -> list:
    """
    Gets the core IDs for all wires/cables connected to a device

    Args:
        device: Device ID
        nc: Whether to include N/C pins (will have no cores) as 0s in the list. Default False
    Returns:
        List of cores found connected to the device
    """
    Pin = _job.CreatePinObject()
    _device.SetId(device)

    cores = []
    for p in _device.GetPinIds(_)[1][1:]:
        Pin.SetId(p)

        c = list(Pin.GetCoreIds(_)[1][1:])
        if len(c) == 0 and nc:
            cores.append(0)
        cores += c
    return cores

def filterByCode(devices: list, code: str) -> list:
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
        return re.sub(r"\d", "", _device.GetName())

    return [d for d in devices if getCode(d) == code]

def filterByAssignment(devices: list, assignment: str) -> list:
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

def filterByLocation(devices: list, location: str) -> list:
    """
    Filters a list of devices based on the device location

    Args:
        devices: List of device IDs
        location: Device location to filter by

    Returns:
        List of devices matching the filter location
    """

    def getLocation(device) -> str:
        _device.SetId(device)
        return _device.GetLocation()[1:]

    return [d for d in devices if getLocation(d) == location]

def filterByAttribute(devices: list, attribute: str, value: str, component=False) -> list:
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

def filterByClass(devices: list, cls: str) -> list:
    """
    Filters a list of devices based on the device class

    Args:
        devices: List of device IDs
        cls: Class to filter by

    Returns:
        List of devices matching the filter class
    """
    return filterByAttribute(devices, "Class", cls, True)

def filterByRegex(devices: list, pattern: str | re.Pattern) -> list:
    """
    Filters a list of devices by name using a regex pattern. Function will use 're.match'

    Args:
        devices: List of device IDs
        pattern: Regex pattern, either as a string or precompiled pattern

    Returns:
        List of devices matching the regex
    """
    def getName(device):
        _device.SetId(device)
        return _device.GetName()

    if type(pattern) is str:
        pattern = re.compile(pattern)
    return [d for d in devices if re.match(pattern, getName(d))]

def filterByComponent(devices: list, component: str) -> list:
    """
    Filters a list of devices based on the component name (exact match)

    Args:
        devices: List of device IDs
        component: Component name

    Returns:
        List of devices with that component
    """
    def getComponent(device):
        _device.SetId(device)
        return _device.GetComponentName()
    return [d for d in devices if getComponent(d) == component]

def getAssignments(devices: list[int]) -> list[str]:
    """
    Returns all assignments from a list of devices in a unique, sorted list

    Args:
        devices: list of devices IDs

    Returns:
        Sorted list of assignments related to those devices
    """
    def assignment(device: int):
        _device.SetId(device)
        return _device.GetAssignment()[1:]

    return list(sorted({assignment(d) for d in devices}))

def getLocations(devices: list[int]) -> list[str]:
    """
    Returns all locations from a list of devices in a unique, sorted list

    Args:
        devices: list of devices IDs

    Returns:
        Sorted list of locations related to those devices
    """
    def location(device: int):
        _device.SetId(device)
        return _device.GetLocation()[1:]

    return list(sorted({location(d) for d in devices}))

__all__ = [f for f in dir() if not f.startswith("_") and f != 're']
