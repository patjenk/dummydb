import json
import datetime
import dateutil.parser


DEFAULT_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S UTC'
DEFAULT_ARGUMENT = "datetime_format"

class DummyDBJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, type):
            return str(obj)
        else:
            return json.JSONEncoder.default(obj)


json._default_encoder = DummyDBJSONEncoder()


def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=None, indent=None, separators=None,
          default=None, sort_keys=False, **kw):
    return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                      check_circular=check_circular, allow_nan=allow_nan,
                      cls=cls, indent=indent, separators=None,
                      default=default, sort_keys=sort_keys, **kw)


def loads(json_str, **kwargs):
    source = json.loads(json_str, **kwargs)
    return iteritems(source)


def iteritems(source):
    for key, val in source.items():
        if isinstance(val, list):
            for a in val:
                iteritems(a)
        elif isinstance(val, dict):
            iteritems(val)
        elif isinstance(val, str):
            try:
                source[key] = dateutil.parser.parse(val, ignoretz=True)
            except:
                pass

            if val == "<class 'int'>":
                source[key] = int
            elif val == "<class 'str'>":
                source[key] = str
            elif val == "<class 'bool'>":
                source[key] = bool
            elif val == "<class 'float'>":
                source[key] = float

    return source
