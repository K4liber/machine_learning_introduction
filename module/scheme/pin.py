import json
import logging
from typing import List, Dict, Any

from .job_rest_client import JobRestClient
from .utils import JsonRepr, camel_to_snake


class PinTypes:
    INPUT = 'input'
    OUTPUT = 'output'


class AccessTypes:
    FTP = 'ftp'


class PinMetaData(JsonRepr):
    def __init__(self, attributes: Dict[str, Any]):
        for required_attribute in PinMetaData.get_required_attributes():
            if required_attribute in attributes:
                self.__setattr__(required_attribute, attributes[required_attribute])
            else:
                raise ValueError('required attribute "' + required_attribute + '" is missing in config')

        for default_attribute, default_value in PinMetaData.get_default_attributes().items():
            if default_attribute in attributes:
                self.__setattr__(default_attribute, attributes[default_attribute])
            else:
                self.__setattr__(default_attribute, default_value)

    def getattr(self, name: str):
        attr_value: str = self.__getattribute__(name)

        if attr_value is None or attr_value == '':
            raise ValueError('attribute "' + name + '" is missing')
        else:
            return attr_value

    @classmethod
    def get_required_attributes(cls):
        return {
            'pin_name',
            'pin_type',
        }

    @classmethod
    def get_default_attributes(cls):
        return {
            'access_path': None,
            'access_type': '',
            'access_credential': None,
            'token_multiplicity': '',
            'data_multiplicity': '',
            'values': None,
        }


def load_pin_meta_data(pin_json: dict) -> PinMetaData:
    try:
        pin_meta_data = PinMetaData({camel_to_snake(key): value for key, value in pin_json.items()})
    except TypeError as type_error:
        errors_msg: str = 'wrong config for pin json:' + str(pin_json) + ', error: ' + str(type_error)
        raise ValueError(errors_msg) from type_error
    # Check required attributes loading
    for required_attribute in PinMetaData.get_required_attributes():
        pin_meta_data.getattr(required_attribute)

    return pin_meta_data


# Load and return input and output pins meta data from the given config file path
def load_pins(config_file_path: str, rest_client: JobRestClient) -> (List[PinMetaData], List[PinMetaData]):
    with open(config_file_path) as json_file:
        try:
            config = json.load(json_file)
            return load_pins_from_json(config)
        except ValueError as value_error:
            error_msg = 'error while loading config from ' + config_file_path + ': ' + str(value_error)
            rest_client.send_ack_token(is_final=True, is_failed=True, note=error_msg)
            logging.error(error_msg)


def load_pins_from_json(config: List[dict]) -> (List[PinMetaData], List[PinMetaData]):
    input_pins: List[PinMetaData] = []
    output_pins: List[PinMetaData] = []

    for pin_description in config:
        try:
            pin = load_pin_meta_data(pin_description)

            if pin.pin_type == PinTypes.INPUT:
                input_pins.append(pin)
                logging.info('loaded pin: ' + pin.to_json())
            elif pin.pin_type == PinTypes.OUTPUT:
                output_pins.append(pin)
                logging.info('loaded pin: ' + pin.to_json())
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
