"""
Imgur CLI
"""

import argparse
import logging
import os
import sys

import imgurpython

from collections import namedtuple

from . import __version__

try:
    from imgur_cli.config import config
except ImportError:
    config = None

logger = logging.getLogger(__name__)


def imgur_credentials():
    ImgurCredentials = namedtuple('ImgurCredentials',
                                  ['client_id', 'client_secret', 'access_token',
                                   'refresh_token', 'mashape_key'])
    if config:
        client_id = config.get('IMGUR_CLIENT_ID')
        client_secret = config.get('IMGUR_CLIENT_SECRET')
        access_token = config.get('IMGUR_ACCESS_TOKEN')
        refresh_token = config.get('IMGUR_REFRESH_TOKEN')
        mashape_key = config.get('IMGUR_MASHAPE_KEY')
    else:
        client_id = os.environ.get('IMGUR_CLIENT_ID')
        client_secret = os.environ.get('IMGUR_CLIENT_SECRET')
        access_token = os.environ.get('IMGUR_ACCESS_TOKEN')
        refresh_token = os.environ.get('IMGUR_REFRESH_TOKEN')
        mashape_key = os.environ.get('IMGUR_MASHAPE_KEY')
    if not client_id or not client_secret:
        raise imgurpython.client.ImgurClientError('Client credentials not found. '
                                                  'Ensure you have both client id '
                                                  'and client secret')
    return ImgurCredentials(client_id, client_secret, access_token,
                            refresh_token, mashape_key)


class ImgurCli():

    @property
    def base_parser(self):
        parser = argparse.ArgumentParser(prog='imgur', description=__doc__.strip(),
                                         epilog='See "imgur help COMMAND" for '
                                         'help on a specific command')

        # Global arguments
        parser.add_argument('-v', '--version', action='version',
                            version=__version__)

        return parser

    def main(self, argv):
        parser = self.base_parser
        options, args = parser.parse_known_args(argv)
        print("help: ", options, args)


def main():
    try:
        imgur_cli = ImgurCli()
        imgur_cli.main(sys.argv[1:])
    except Exception as e:
        logger.debug(e, exc_info=1)
        print(e, file=sys.stderr)
        sys.exit(1)

# Remove below in the end
if __name__ == '__main__':
    main()
