import json
import re


class JsonRepr:
    def to_json(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=3)

    def __repr__(self):
        return self.to_json()


def camel_to_snake(name: str) -> str:
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()


def snake_to_camel(name: str) -> str:
    return ''.join(word.title() for word in name.split('_'))
