from imgur_cli.exceptions import CommandError
from imgur_cli.utils import cli_arg


def cmd_gallery(client, args):
    """Print items from Imgur gallery"""
    gallery = client.gallery()
    for item in gallery:
        print(item.link)
