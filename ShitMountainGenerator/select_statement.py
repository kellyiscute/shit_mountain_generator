import re
from typing import Dict, Any, Optional, List
from xml.etree.ElementTree import Element

from ShitMountainGenerator.common import parse_attr
from ShitMountainGenerator.exceptions import InvalidTemplateDeclerationException


class SelectCase:
    test: str
    content: str

    def __init__(self, test: str, content: str):
        self.test = test
        self.content = content

    def perform_test(self, var: str) -> bool:
        if type(var) is int or type(var) is float:
            try:
                return var == float(self.test)
            except:
                return False
        elif type(var) is bool:
            return str(var) == self.test
        elif type(var) is str:
            return var == str(self.test)


class SelectStatement:
    name: str
    var_name: str
    body: Element
    cases: List[SelectCase]
    default: Optional[str]

    def __init__(self, name: str, var_name: str, body: List[str]):
        self.name = name
        self.var_name = var_name
        self.cases = []
        self.default = None
        block = []
        for line in body:
            if line.startswith("<case"):
                block = [line]
            elif line.startswith("<default"):
                block = []
            elif line.startswith("</case"):
                self.cases.append(self._parse_case(block[:]))
            elif line.startswith("</default"):
                self.default = "".join(block)
            else:
                block.append(re.sub(r"^\t|( {4})", "", line, 1))

    def _parse_case(self, lines: List[str]) -> SelectCase:
        attrs = parse_attr(lines[0])
        if "test" not in attrs:
            raise InvalidTemplateDeclerationException("attribute `test` required for case statement")
        return SelectCase(attrs["test"], "".join(lines[1:]))

    def select_shit(self, context: Dict[str, Any]) -> Optional[str]:
        for case in self.cases:
            if case.perform_test(context[self.var_name]):
                return case.content
        else:
            if self.default is not None:
                return self.default
            else:
                raise Exception(f"No default value defined but nothing matches: \n    select: {self.name}\n    var: {self.var_name}\n    target value: {context[self.var_name]}\n")
