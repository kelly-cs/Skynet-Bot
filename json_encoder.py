import json
from decimal import Decimal
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        # Any other serializer if needed
        return super(CustomJSONEncoder, self).default(o)