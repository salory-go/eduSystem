import json


def process(text: str):
    text = (text.replace('\n', '')
            .replace('\r', '')
            .replace('\t', '')
            .strip())
    return json.loads(text)
