from typing import Union
import datetime
from dateutil import parser


def parse(t: Union[str,datetime]):
    if type(t) == str:
        return int(parser.parse(t).timestamp())
    else:
        return int(t.timestamp())

