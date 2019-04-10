from abc import ABC
from enum import Enum
from typing import List

PROPERTY_DEFINITIONS = 'PropertyDefinitions'
TECHNOLOGY = 'Technology'
TYPE = 'Type'
MODEL = 'Model'
PROPERTIES = 'Properties'
ONLINE = 'Online'
NAME = 'Name'
IDENTIFIER = 'Identifier'
UUID = 'Uuid'
TRUE = 'true'
CAN_CONTROL = 'CanControl'
HAS_STATUS = 'HasStatus'
DESCRIPTION = 'Description'
LOCATION_ICON = 'LocationIcon'
LOCATION_NAME = 'LocationName'
LOCATION_ID = 'LocationId'
STATUS = 'Status'
PARAMETERS = 'Parameters'


class NHC2DeviceStatusPropertyValue(Enum):
    OFF = 'Off'
    ON = 'On'


class NHC2DeviceModel(Enum):
    LIGHT = 'light'
    SWITCHED_GENERIC = 'switched-generic'


class NHC2DeviceType(Enum):
    ACTION = 'action'


class NHC2DeviceTechnology(Enum):
    NIKOHOMECONTROL = 'nikohomecontrol'


class NHC2Device:
    def __init__(self):
        Uuid: str = None
        Identifier: str = None
        Name: str = None
        Technology: NHC2DeviceTechnology = None
        Online: bool = None
        Model: NHC2DeviceModel = None
        Type: NHC2DeviceType = None
        Properties: List[NHC2DeviceProperty] = None
        PropertyDefinitions: List[NHC2DevicePropertyDefinition] = None
        Parameters: List[NHC2DeviceParameter] = None


class NHC2DeviceProperty(ABC):
    def __init__(self):
        super().__init__()


class NHC2DeviceParameter(ABC):
    def __init__(self):
        super().__init__()


class NHC2DevicePropertyDefinition(ABC):
    def __init__(self):
        super().__init__()


class NHC2DeviceStatusPropertyDefinition(NHC2DevicePropertyDefinition):
    def __init__(self):
        super().__init__()
        self.Status: NHC2DeviceStatusPropertyDefinitionDetails = None


class NHC2DeviceStatusPropertyDefinitionDetails:
    def __init__(self):
        super().__init__()
        self.Description: str = None
        self.HasStatus: bool = None
        self.CanControl: bool = None


class NHC2DeviceLocationIdParameter(NHC2DeviceParameter):
    def __init__(self):
        super().__init__()
        self.LocationId: str = None


class NHC2DeviceLocationNameParameter(NHC2DeviceParameter):
    def __init__(self):
        super().__init__()
        self.LocationName: str = None


class NHC2DeviceLocationIconParameter(NHC2DeviceParameter):
    def __init__(self):
        super().__init__()
        self.LocationIcon: str = None


class NHC2DeviceStatusProperty(NHC2DeviceProperty):
    def __init__(self):
        super().__init__()
        self.Status: bool = None


def generateNHC2Device(nhc2device)-> NHC2Device:
    def generateNHC2LocationIdParameter(prop):
        location_id_property = NHC2DeviceLocationIdParameter()
        location_id_property.LocationId = prop[LOCATION_ID]
        return location_id_property

    def generateNHC2LocationNameParameter(prop):
        location_name_property = NHC2DeviceLocationNameParameter()
        location_name_property.LocationName = prop[LOCATION_NAME]
        return location_name_property

    def generateNHC2LocationLocationIconParameter(prop):
        location_icon_property = NHC2DeviceLocationIconParameter()
        location_icon_property.LocationIcon = prop[LOCATION_ICON]
        return location_icon_property

    def generateNHC2StatusProperty(prop):
        status_property = NHC2DeviceStatusProperty()
        status_property.Status = NHC2DeviceStatusPropertyValue(prop[STATUS])
        return status_property

    def generateNHC2Properties(properties):
        props: List[NHC2DeviceProperty] = []
        for prop in properties:
            if STATUS in prop:
                props.append(generateNHC2StatusProperty(prop))
        return props

    def generateNHC2StatusPropertyDefinitions(definition):
        statusPropertyDef: NHC2DeviceStatusPropertyDefinition = NHC2DeviceStatusPropertyDefinition()
        statusPropertyDef.Status = NHC2DeviceStatusPropertyDefinitionDetails()
        statusPropertyDef.Status.Description = definition[STATUS][DESCRIPTION]
        statusPropertyDef.Status.HasStatus = definition[STATUS][HAS_STATUS].lower() == TRUE
        statusPropertyDef.Status.CanControl = definition[STATUS][CAN_CONTROL].lower() == TRUE
        return statusPropertyDef

    def generateNHC2PropertyDefinitions(properties):
        popDefs: List[NHC2DevicePropertyDefinition] = []
        for prop in properties:
            if STATUS in prop:
                popDefs.append(generateNHC2StatusPropertyDefinitions(prop))
        return popDefs

    def generateNHC2Parameters(parameters):
        params: List[NHC2DeviceParameter] = []
        for param in parameters:
            if LOCATION_ID in param:
                params.append(generateNHC2LocationIdParameter(param))
            if LOCATION_NAME in param:
                params.append(generateNHC2LocationNameParameter(param))
            if LOCATION_ICON in param:
                params.append(generateNHC2LocationLocationIconParameter(param))
        return params

    device = NHC2Device()
    if UUID in nhc2device:
        device.Uuid = nhc2device[UUID]
    if IDENTIFIER in nhc2device:
        device.Identifier = nhc2device[IDENTIFIER]
    if NAME in nhc2device:
        device.Name = nhc2device[NAME]
    if ONLINE in nhc2device:
        device.Online = nhc2device[ONLINE].lower() == TRUE
    if PROPERTIES in nhc2device:
        device.Properties = generateNHC2Properties(nhc2device[PROPERTIES])
    if MODEL in nhc2device:
        device.Model = NHC2DeviceModel(nhc2device[MODEL])
    if TYPE in nhc2device:
        device.Type = NHC2DeviceType(nhc2device[TYPE])
    if TECHNOLOGY in nhc2device:
        device.Technology = NHC2DeviceTechnology(nhc2device[TECHNOLOGY])
    if PROPERTY_DEFINITIONS in nhc2device:
        device.PropertyDefinitions = generateNHC2PropertyDefinitions(nhc2device[PROPERTY_DEFINITIONS])
    if PARAMETERS in nhc2device:
        device.Parameters = generateNHC2Parameters(nhc2device[PARAMETERS])
    return device


