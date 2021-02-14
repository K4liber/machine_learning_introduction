import unittest
from typing import List

from ..scheme.pin import load_pins_from_json


class TestLoadPinsFromJson(unittest.TestCase):
    def test_simple_correct_json(self):
        json: List[dict] = [
            {
                "PinName": "Input",
                "PinType": "input",
                "AccessType": "ftp",
                "AccessCredential": {
                    "connectionstring": "ftp://username:password@input_host:port"
                }
            },
            {
                "PinName": "Output",
                "PinType": "output",
                "AccessType": "ftp",
                "AccessCredential": {
                    "connectionstring": "ftp://username:password@output_host:port"
                }
            }
        ]
        input_pins, output_pins = load_pins_from_json(json)
        self.assertEqual(len(input_pins), 1)
        self.assertEqual(len(output_pins), 1)

    def test_missing_access_credentials(self):
        json: List[dict] = [
            {
                "PinName": "Input",
            },
        ]
        try:
            load_pins_from_json(json)
            self.assertTrue(False, "test case should raise an error")
        except ValueError:
            pass

    def test_origin_pin_config(self):
        json: List[dict] = [
            {
                'PinName': 'Input',
                'PinType': 'input',
                'AccessType': '',
                'DataMultiplicity': 'multiple',
                'TokenMultiplicity': 'multiple'
            },
            {
                'PinName': 'Output',
                'PinType': 'output',
                'AccessType': '',
                'DataMultiplicity': 'multiple',
                'TokenMultiplicity': 'multiple'
            }
        ]
        input_pins, output_pins = load_pins_from_json(json)
        self.assertEqual(len(input_pins), 1)
        self.assertEqual(len(output_pins), 1)


if __name__ == '__main__':
    unittest.main()
