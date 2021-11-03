from typing import Dict, Any, Optional, List
from xml.etree.ElementTree import Element


class SelectCase:
    test: str
    content: str

    def __init__(self, test: str, content: str):
        self.test = test
        self.content = content

    def perform_test(self, var) -> bool:
        if type(var) is int or type(var) is float:
            try:
                return var == float(self.test)
            except:
                return False
        elif type(var) is bool:
            try:
                return var == bool(self.test)
            except:
                return False
        elif type(var) is str:
            return var == str(self.test)


class SelectStatement:
    name: str
    var_name: str
    body: Element
    cases: List[SelectCase]
    default: Optional[str]

    def __init__(self, body: Element):
        self.name = body.get("name")
        self.body = body
        self.var_name = body.get("var")
        self.cases = []
        self.default = None
        children = body.getchildren()
        for child in children:
            if child.tag == "case":
                self.cases.append(SelectCase(child.get("test"), child.text))
            elif child.tag == "default":
                self.default = child.text

    def select_shit(self, context: Dict[str, Any]) -> Optional[str]:
        for case in self.cases:
            if (case.perform_test(context[self.var_name])):
                return case.content
        else:
            return self.default
