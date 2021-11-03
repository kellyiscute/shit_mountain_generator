class Template:
    name: str
    raw_content: str

    def __init__(self, name: str, raw_content: str):
        self.name = name
        self.raw_content = raw_content

    def generate(self) -> str:
        return ""
