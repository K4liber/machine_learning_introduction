import unittest
from typing import List

from .token import XInputTokenMessage
from .pin import load_pins_from_json


class TestLoadInputToken(unittest.TestCase):
    def test_simple_correct_json(self):
        token_json: dict = {
            "MsgUid": "1",
            "PinName": "Input",
            "Values": "file.txt",
        }
        try:
            blsc_token = XInputTokenMessage(**token_json)
            print(blsc_token)
        except TypeError as te:
            self.assert_(False, te)


if __name__ == '__main__':
    unittest.main()
