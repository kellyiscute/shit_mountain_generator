import re


class Template:
    name: str
    raw_content: str

    def __init__(self, name: str, raw_content: str):
        self.name = name
        self.raw_content = re.sub(r"^\t|[ ]{4}", "", raw_content, flags=re.RegexFlag.MULTILINE)

    def generate(self) -> str:
        return ""
