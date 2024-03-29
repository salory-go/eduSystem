from typing import Union
from datetime import datetime
from dateutil import parser


def parse(t: Union[str, datetime]):
    if isinstance(t, str):
        return int(parser.parse(t).timestamp())
    else:
        return int(t.timestamp())
