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
from imgur_cli import exceptions
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


class ImgurCli:

    def __init__(self):
        self.subcommands = {}
        self.parser = None
        self.client = None
        self.subparsers = {}

    @property
    def base_parser(self):
        parser = argparse.ArgumentParser(prog='imgur', description=__doc__.strip(),
                                         epilog='See "imgur help <SUBPARSER> '
                                         '<SUBCOMMAND>" for help on a specific '
                                         'subparser or subcommand')

        # Global arguments
        parser.add_argument('-v', '--version', action='version',
                            version='%(prog)s {0}'.format(__version__))

        return parser

    def generate_parser(self):
        self.parser = self.base_parser
        base_subparser = self.parser.add_subparsers(metavar='<subparsers>')
        self._add_help(self, base_subparser)
        self._add_subparsers(base_subparser)
        self._add_subcommands(cli_api)

    def _generate_subcommand(self, name, callback, subparser):
        description = callback.__doc__ or ''
        action_help = description.strip()
        arguments = getattr(callback, 'arguments', [])
        subcommand = subparser.add_parser(name, help=action_help,
                                          description=description,
                                          add_help=False)
        subcommand.add_argument('-h', '--help', action='help',
                                help=argparse.SUPPRESS)
        for args, kwargs in arguments:
            subcommand.add_argument(*args, **kwargs)
        subcommand.set_defaults(func=callback)
        self.subcommands[name] = subcommand

    def _add_help(self, cli_api, subparser):
        callback = getattr(self, 'cmd_help')
        self._generate_subcommand('help', callback, subparser)

    def _add_subparsers(self, subparser):
        for name, description in cli_api.SUBPARSERS.items():
            parser = subparser.add_parser(name, help=description,
                                          description=description,
                                          add_help=False)
            parser.add_argument('-h', '--help', action='help',
                                help=argparse.SUPPRESS)
            self.subparsers[name] = {}
            self.subparsers[name]['parser'] = parser
            self.subparsers[name]['subparser'] = (
                parser.add_subparsers(metavar='<subcommands>')
            )

    def _add_subcommands(self, cli_api):
        for attr in (action for action in dir(cli_api)
                     if action.startswith('cmd_')):
            name = '-'.join(attr.split('_')[2:])
            callback = getattr(cli_api, attr)
            subparser_name = getattr(callback, 'subparser', None)
            subparser = self.subparsers[subparser_name]['subparser']
            self._generate_subcommand(name, callback, subparser)

    @cli_arg('subparser', metavar='<subparser>', nargs='?',
             help='Display help for <subparser>')
    @cli_arg('subcommand', metavar='<subcommand>', nargs='?',
             help='Display help for <subcommand>')
    def cmd_help(self, args):
        """Display help about this program or one of its subparsers"""
        if args.subparser:
            if args.subcommand:
                try:
                    self.subcommands[args.subcommand].print_help()
                except KeyError:
                    raise exceptions.CommandError('{0} is not valid subcommand'
                                                  .format(args.subcommand))
            else:
                try:
                    self.subparsers[args.subparser]['parser'].print_help()
                except KeyError:
                    raise exceptions.CommandError('{0} is not valid subparser'
                                                  .format(args.subparser))
        else:
            self.parser.print_help()

    def main(self, argv):
        self.generate_parser()
        if not argv:
            self.parser.print_help()
            return 0
        args = self.parser.parse_args(argv)
        try:
            # Short-circuit and deal with help right away
            if args.func == self.cmd_help:
                self.cmd_help(args)
                return 0
            credentials = imgur_credentials()
            self.client = imgurpython.ImgurClient(*credentials)
            args.func(self.client, args)
        except AttributeError:
            self.subparsers[argv[0]]['parser'].print_help()


def main():
    try:
        imgur_cli = ImgurCli()
        imgur_cli.main(sys.argv[1:])
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
