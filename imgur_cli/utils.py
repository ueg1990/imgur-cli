import json


def cli_arg(*args, **kwargs):
    """Decorator for CLI args"""
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


def add_arg(func, *args, **kwargs):
    """Bind CLI arguments to a 'cmd_' format function"""
    if not hasattr(func, 'arguments'):
        func.arguments = []

    if (args, kwargs) not in func.arguments:
        # Because of the semantics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.arguments.insert(0, (args, kwargs))


def cli_subparser(*args, **kwargs):
    """Decorator for CLI subparsers"""
    def _decorator(func):
        add_subparser(func, *args, **kwargs)
        return func
    return _decorator


def add_subparser(func, *args, **kwargs):
    """Bind a subparser to a 'cmd_' format function"""
    if not hasattr(func, 'subparser'):
        func.subparser = args[0]


def generate_output(result, output_filename=None):
    """Generate JSON output and either print it to console or save to a file"""
    if output_filename:
        with open(output_filename, 'w') as json_file:
            data = json.dumps(result, json_file, indent=4, separators=(',', ': '))
            json_file.write(data)
    else:
        print(json.dumps(result, indent=4, separators=(',', ': ')))


def data_fields(args, allowed_fields):
    """Generate data fields dictionary required by some client methods"""
    data = {}
    for field in allowed_fields:
        field_value = getattr(args, field, None)
        if field_value:
            data[field] = field_value
    return data
