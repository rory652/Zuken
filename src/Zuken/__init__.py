"""
Small module that contains a variety of functions to help with script development
Focus is on schematic/formboard development as that's what I've worked on at my own job
"""

from .e3 import E3
from .e3 import Job
from .e3 import print
from .e3 import warn
from .e3 import error
from .e3 import message
from .e3 import verify

from .devices import devicesOnSheet
from .devices import deviceFormboardId
from .devices import tableSymbolId
from .devices import coreIds
from .devices import filterByDeviceCode
from .devices import filterByDeviceAssignment
from .devices import filterByDeviceLocation
from .devices import filterByDeviceAttribute
from .devices import filterByDeviceClass
from .devices import filterByDeviceRegex
from .devices import filterByComponent

from .symbols import placeSymbol
from .symbols import extractSymbolText
from .symbols import filterBySymbolName
