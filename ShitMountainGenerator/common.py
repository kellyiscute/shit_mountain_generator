import re
from typing import Dict

_attr_parse_pattern = re.compile(r'\s*([A-z\-_]*)="([^"]*)"')


def parse_attr(line: str) -> Dict[str, str]:
    attrs = _attr_parse_pattern.finditer(line)
    attr_dict = {}
    for attr in attrs:
        attr_name, attr_value = attr.group(1), attr.group(2)
        attr_dict[attr_name] = attr_value
    return attr_dict
