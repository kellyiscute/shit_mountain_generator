from typing import List
import re
from ShitMountainGenerator.template import Template
from ShitMountainGenerator.select_statement import SelectStatement


def parse_tmpl(block: str) -> Template:
    # TODO: unfinished
    pass


def parse(data: str):
    lines = data.splitlines(True)
    templates: List[Template] = []
    select_statements: List[SelectStatement] = []
    block = ""
    leading_indent = re.compile(r"^\t|[ ]{4}")
    for line in lines:
        if (line.startswith("<tmpl")):
            block = line
        elif line.startswith("</tmpl>"):
            templates.append(parse_tmpl(block))
        elif line.startswith("<select"):
            block = line
        elif line.startswith("</select>"):
            pass  # TODO
        else:
            # remove leading indent
            block += leading_indent.sub("", line)



if __name__ == '__main__':
    f = open("data_class.tmpl", "r")
    parse(f.read())
