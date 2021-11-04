import re
from typing import List, Dict, Any

from ShitMountainGenerator.select_statement import SelectStatement
from ShitMountainGenerator.template import Template
from ShitMountainGenerator.template_parser import parse

Context = Dict[str, Any]


class Shitter:
    templates: Dict[str, Template]
    select_statements: Dict[str, SelectStatement]

    def __init__(self, templates: List[Template], select_statements: List[SelectStatement]):
        self.select_statements = {}
        for select_statement in select_statements:
            self.select_statements[select_statement.name] = select_statement
        self.templates = {}
        for template in templates:
            self.templates[template.name] = template

        # group1: var/operation name
        self._var_pattern = re.compile(r'{{\s*([A-z_\-()]*)\s*}}')
        # group1: template name, group2: context
        self._loop_pattern = re.compile(r'{%\s*([A-z_\-()]*)\s*<-\s*([A-z_\-()]*)\s*%}')
        self._indent_detection_pattern = re.compile(r"^[ \t]*")

    @classmethod
    def from_template(cls, path: str):
        with open(path, "r") as f:
            data = f.read()
        return cls(*parse(data))

    def _detect_indent(self, line: str) -> str:
        indent = self._indent_detection_pattern.search(line)
        return indent.group(0)

    def _add_indent(self, block: str, indent: str) -> List[str]:
        result = []
        block = block.splitlines()
        for line in block:
            result.append(indent + line)

        return result

    def _loop(self, template: str, line: str, field: str, context: Context) -> str:
        template = self.templates[template]
        result_lines = []
        # need to detect indent
        indent = self._detect_indent(line)
        for inner_context in context[field]:
            template_result = self._run_template(template, inner_context)
            result_lines.extend(self._add_indent(template_result, indent))

        return "\n".join(result_lines)

    def _process_var_operation(self, line: str, expression: str, context: Context) -> str:
        if expression.startswith("use("):
            replacement = self.select_statements[expression.replace("use(", "")[:-1]].select_shit(context)
        else:
            replacement = str(context[expression])

        line = self._var_pattern.sub(replacement, line, 1)

        match = self._var_pattern.search(line)
        if match is not None:
            line = self._process_var_operation(line, match.group(1), context)
            match = self._loop_pattern.search(line)
        if match is not None:
            replacement = self._loop(match.group(1), line, match.group(2), context)
            line = self._loop_pattern.sub(replacement, line, 1)

        return line

    def _run_template(self, template: Template, context: Context) -> str:
        result_lines: List[str] = []

        content = template.raw_content.splitlines()
        for line in content:
            result_line = line
            if (match := self._var_pattern.search(line)) is not None:
                result_line = self._process_var_operation(line, match.group(1), context)
            if (match := self._loop_pattern.search(line)) is not None:
                result_line = self._loop(match.group(1), line, match.group(2), context)

            result_lines.append(result_line)

        return "\n".join(result_lines)

    def shit(self, context: Context) -> str:
        return self._run_template(self.templates["$main$"], context)
