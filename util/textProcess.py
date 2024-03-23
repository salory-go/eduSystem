import json


def process(text: str):
    text = text.replace('\n', '').replace('\r', '').replace('\t', '')
    return json.loads(text)
