import json


def cli_arg(*args, **kwargs):
    """Decorator for CLI args"""
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


def add_arg(func, *args, **kwargs):
    """Bind CLI arguments a 'cmd_' format function"""
    if not hasattr(func, 'arguments'):
        func.arguments = []

    if (args, kwargs) not in func.arguments:
        # Because of the semantics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.arguments.insert(0, (args, kwargs))


def generate_output(output_filename, result):
    if not output_filename:
        print(json.dumps(result, indent=4, separators=(',', ': ')))
    else:
        with open(output_filename, 'w') as json_file:
            data = json.dumps(result, json_file, indent=4, separators=(',', ': '))
            json_file.write(data)
