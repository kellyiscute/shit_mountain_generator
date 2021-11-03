import re
from typing import List, Tuple

from ShitMountainGenerator.common import parse_attr
from ShitMountainGenerator.exceptions import InvalidTemplateDeclerationException
from ShitMountainGenerator.select_statement import SelectStatement
from ShitMountainGenerator.template import Template


def parse_tmpl(block: str) -> Template:
    lines = block.splitlines()
    attr_dict = parse_attr(lines[0])
    lines = lines[1:]
    return Template(attr_dict["name"] if "name" in attr_dict else "$main$", "\n".join(lines))


def parse_select(block: str) -> SelectStatement:
    lines = block.splitlines(True)
    attrs = parse_attr(lines[0])
    if "name" not in attrs or "var" not in attrs:
        raise InvalidTemplateDeclerationException(
                "attribute `name` and `var` required for select statement")
    return SelectStatement(name=attrs["name"], var_name=attrs["var"], body=lines[1:])


def parse(data: str) -> Tuple[List[Template], List[SelectStatement]]:
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
            select_statements.append(parse_select(block))
        else:
            # remove leading indent
            block += leading_indent.sub("", line)

    return templates, select_statements
