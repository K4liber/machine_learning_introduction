import unittest
from .token import InputToken


class TestLoadInputToken(unittest.TestCase):
    def test_simple_correct_json(self):
        token_json: dict = {
            'MsgUid': '1',
            'PinName': 'Input',
            'Values': '{\"ResourcePath\": \"/files/recogniser/in\"}'
        }
        try:
            token = InputToken(**token_json)
            print(token)
        except TypeError as te:
            self.assert_(False, te)

    def test_incorrect_json(self):
        token_json: dict = {
            'MsgUid': '1',
            'PinName': 'Input',
            'Values': '{\"ResourcePath\": \"/files/recogniser/in\"}',
            'SthElse': ''
        }
        try:
            InputToken(**token_json)
            self.assert_(False, 'test failed, should raise an error')
        except TypeError as te:
            print(te)


if __name__ == '__main__':
    unittest.main()
