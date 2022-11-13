import decimal
from flask import json

class MyJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(round(obj, 2))
        return super(MyJSONEncoder, self).default(obj)