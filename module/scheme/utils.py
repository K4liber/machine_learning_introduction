import json
import re
from hashlib import md5
from time import localtime


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


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def get_random_output_folder(input_folder: str) -> str:
    from pathlib import Path
    path = Path(input_folder)
    return str(path.parent) + '/out_' + md5(str(localtime()).encode('utf-8')).hexdigest()[:10]
