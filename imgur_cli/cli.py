"""
Imgur CLI
"""

import argparse
import logging
import os
import sys

from collections import namedtuple

import imgurpython

from imgur_cli import __version__
from imgur_cli import cli_api
from imgur_cli.exceptions import CommandError
from imgur_cli.utils import cli_arg

logger = logging.getLogger(__name__)


def imgur_credentials():
    ImgurCredentials = namedtuple('ImgurCredentials',
                                  ['client_id', 'client_secret', 'access_token',
                                   'refresh_token', 'mashape_key'])

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
                            version='%(prog)s {0}'.format(__version__))

        parser.add_argument('--debug', default=False, action='store_true',
                            help='Print debugging output')

        return parser

    def setup_debugging(self):
        streamformat = "%(levelname)s (%(module)s:%(lineno)d) %(message)s"
        # Set up the root logger to debug so that the submodules can print
        # debug messages
        logging.basicConfig(level=logging.DEBUG, format=streamformat)

    @property
    def subcommand_parser(self):
        parser = self.base_parser
        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        actions_module = cli_api
        self._find_actions(subparsers, actions_module)
        self._find_actions(subparsers, self)
        return parser

    def _find_actions(self, subparsers, actions_module):
        for attr in (action for action in dir(actions_module)
                     if action.startswith('cmd_')):
            command = attr[4:].replace('_', '-')
            callback = getattr(actions_module, attr)
            description = callback.__doc__ or ''
            action_help = description.strip()
            arguments = getattr(callback, 'arguments', [])
            subparser = subparsers.add_parser(command, help=action_help,
                                              description=description,
                                              add_help=False)
            subparser.add_argument('-h', '--help', action='help',
                                   help=argparse.SUPPRESS)
            self.subcommands[command] = subparser
            for args, kwargs in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    @cli_arg('command', metavar='<subcommand', nargs='?',
             help='Display help for <subcommand>')
    def cmd_help(self, args):
        """Display help about this program or one of its subcommands"""
        if args.command:
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise CommandError('{0} is not valid subcommand'
                                   .format(args.command))
        else:
            self.parser.print_help()

    def main(self, argv):
        credentials = imgur_credentials()
        self.parser = self.subcommand_parser
        if not argv:
            self.parser.print_help()
            return 0
        args = self.parser.parse_args(argv)
        # Short-circuit and deal with help right away
        if args.func == self.cmd_help:
            self.cmd_help(args)
            return 0
        self.client = imgurpython.ImgurClient(*credentials)
        args.func(self.client, args)


def main():
    try:
        imgur_cli = ImgurCli()
        imgur_cli.main(sys.argv[1:])
    except Exception as e:
        logger.debug(e, exc_info=1)
        print(e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
