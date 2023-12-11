from .e3 import Job
from re import sub

_device = Job.CreateDeviceObject()
_ = None

def devicesOnSheet(sheet: int, base=False):
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

def filterByDeviceCode(devices: list, code: str) -> list:
    def getCode(device) -> str:
        _device.SetId(device)
        return sub(r"\d", "", _device.GetName())

    return [d for d in devices if getCode(d) == code]

def filterByDeviceAssignment(devices: list, assignment: str) -> list:
    def getAssignment(device) -> str:
        _device.SetId(device)
        return _device.GetAssignment()[1:]

    return [d for d in devices if getAssignment(d) == assignment]

def filterByDeviceLocation(devices: list, location: str) -> list:
    def getLocation(device) -> str:
        _device.SetId(device)
        return _device.GetLocation()[1:]

    return [d for d in devices if getLocation(d) == location]

def filterByDeviceAttribute(devices: list, attribute: str, value: str, component=False) -> list:
    def getAttribute(device) -> str:
        _device.SetId(device)

        if component:
            return _device.GetComponentAttributeValue(attribute)
        else:
            return _device.GetAttributeValue(attribute)

    return [d for d in devices if getAttribute(d) == value]

def filterByDeviceClass(devices: list, cls: str) -> list:
    return filterByDeviceAttribute(devices, "Class", cls, True)
