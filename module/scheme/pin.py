import json
import logging
from typing import List, Dict

from .utils import JsonRepr, camel_to_snake

_pin_required_attributes = [
    'PinName',
    'PinType',
    'AccessType',
    'AccessCredential',
]


class PinTypes:
    INPUT = 'input'
    OUTPUT = 'output'


class AccessTypes:
    FTP = 'ftp'


class PinMetaData(JsonRepr):
    def __init__(self, pin_name: str, pin_type: str, access_type: str,
                 access_credential: Dict[str, str], values: Dict[str, str] = dict()):
        self.pin_name = pin_name
        self.pin_type = pin_type
        self.access_type = access_type
        self.access_credential = access_credential
        self.values = values

    def getattr(self, name: str):
        attr_value: str = self.__getattribute__(name)

        if attr_value is None or attr_value == '':
            raise ValueError('attribute "' + name + '" is missing')
        else:
            return attr_value


def load_pin_meta_data(pin_json: dict) -> PinMetaData:
    try:
        pin_meta_data = PinMetaData(**{camel_to_snake(key): value for key, value in pin_json.items()})
    except TypeError as type_error:
        errors_msg: str = 'wrong config for pin json:' + str(pin_json) + ', error: ' + str(type_error)
        raise ValueError(errors_msg) from type_error
    # Check required attributes loading
    for required_attribute in _pin_required_attributes:
        pin_meta_data.getattr(camel_to_snake(required_attribute))

    return pin_meta_data


# Load and return input and output pins meta data from the given config file path
def load_pins(config_file_path: str) -> (List[PinMetaData], List[PinMetaData]):
    with open(config_file_path) as json_file:
        try:
            config = json.load(json_file)
            return load_pins_from_json(config)
        except ValueError as value_error:
            logging.error('error while loading config from ' + config_file_path + ': ' + str(value_error))


def load_pins_from_json(config: List[dict]) -> (List[PinMetaData], List[PinMetaData]):
    input_pins: List[PinMetaData] = []
    output_pins: List[PinMetaData] = []

    for pin_description in config:
        try:
            pin = load_pin_meta_data(pin_description)

            if pin.pin_type == PinTypes.INPUT:
                input_pins.append(pin)
                print('loaded pin: ' + pin.to_json())
            elif pin.pin_type == PinTypes.OUTPUT:
                output_pins.append(pin)
                print('loaded pin: ' + pin.to_json())
            else:
                print('unknown type for pin:"' + pin.to_json())
        except ValueError as value_error:
            logging.error('pin loading error: ' + str(value_error))
            raise value_error

    return input_pins, output_pins


class MissingPin(Exception):
    """Exception raised for errors in the pins configuration.

    Attributes:
        pins -- list of pins where we look for a specific pin
        message -- explanation of the error
    """

    def __init__(self, pins: List[PinMetaData], message="missing pin"):
        self.pins = pins
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pins} -> {self.message}'


class MissingPinValue(Exception):
    """Exception raised for errors in the pins configuration.

    Attributes:
        pin_values -- values of a pin
        message -- explanation of the error
    """

    def __init__(self, pin_values: Dict[str, str], message="missing value"):
        self.pin_values = pin_values
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pin_values} -> {self.message}'
