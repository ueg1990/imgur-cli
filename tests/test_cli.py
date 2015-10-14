import argparse
import sys

import fixtures
import imgurpython
import testtools

from unittest import mock

import imgur_cli.cli as cli
from imgur_cli import exceptions

FAKE_ENV = {'IMGUR_CLIENT_ID': 'client_id',
            'IMGUR_CLIENT_SECRET': 'client_secret',
            'IMGUR_ACCESS_TOKEN': 'access_token',
            'IMGUR_REFRESH_TOKEN': 'refresh_token',
            'IMGUR_MASHAPE_KEY': 'mashape_key'}


class TestImgurCli(testtools.TestCase):

    def setUp(self):
        super(TestImgurCli, self).setUp()
        self.mock_client = mock.patch('imgur_cli.cli.imgurpython.ImgurClient')
        self.mock_client.start()
        self.mock_output = mock.patch('imgur_cli.cli_api.generate_output')
        self.mock_output.start()

    def tearDown(self):
        super(TestImgurCli, self).tearDown()
        self.mock_client.stop()
        self.mock_output.stop()

    def cli(self, argv, exclude=None):
        self.make_env(exclude)
        _cli = cli.ImgurCli()
        _cli.main(argv)
        return _cli

    def make_env(self, exclude=None):
        env = {key: value for key, value in FAKE_ENV.items() if key != exclude}
        self.useFixture(fixtures.MonkeyPatch('os.environ', env))

    def test_imgur_credentials_env(self):
        self.make_env()
        expected = ('client_id', 'client_secret', 'access_token', 'refresh_token',
                    'mashape_key')
        imgur_credentials = cli.imgur_credentials()
        self.assertEqual(expected, imgur_credentials)
        self.make_env(exclude='IMGUR_MASHAPE_KEY')
        expected = ('client_id', 'client_secret', 'access_token', 'refresh_token',
                    None)
        imgur_credentials = cli.imgur_credentials()
        self.assertEqual(expected, imgur_credentials)
        self.make_env(exclude='IMGUR_CLIENT_ID')
        self.assertRaises(imgurpython.client.ImgurClientError,
                          cli.imgur_credentials)
        self.make_env(exclude='IMGUR_CLIENT_SECRET')
        self.assertRaises(imgurpython.client.ImgurClientError,
                          cli.imgur_credentials)

    def test_help_unknown_command(self):
        self.assertRaises(exceptions.CommandError, self.cli, ['help', 'foofoo'])

    def test_album(self):
        argv = ['album', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.album_id, argv[1])
        self.assertEqual(parser_args.func.__name__, 'cmd_album')
        self.assertTrue(_cli.client.get_album.called)
        self.assertRaises(SystemExit, self.cli, ['album'])

    def test_image(self):
        argv = ['image', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.image_id, argv[1])
        self.assertEqual(parser_args.func.__name__, 'cmd_image')
        self.assertTrue(_cli.client.get_image.called)
        self.assertRaises(SystemExit, self.cli, ['image'])
