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


class DevNull:
    def write(self, data):
        pass


class TestImgurCli(testtools.TestCase):

    def setUp(self):
        super(TestImgurCli, self).setUp()
        self.mock_client = mock.patch('imgur_cli.cli.imgurpython.ImgurClient')
        self._client = self.mock_client.start()
        self.mock_output = mock.patch('imgur_cli.cli_api.generate_output')
        self.mock_output.start()
        self.old_stderr = sys.stderr
        sys.stderr = DevNull()

    def tearDown(self):
        super(TestImgurCli, self).tearDown()
        self.mock_client.stop()
        self.mock_output.stop()
        sys.stderr = self.old_stderr

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

    def test_gallery(self):
        argv = ['gallery']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.func.__name__, 'cmd_gallery')
        self.assertTrue(_cli.client.gallery.called)
        expected_args = {'section': 'hot', 'sort': 'viral', 'page': 0,
                         'window': 'day', 'show_viral': False, 'output_file': None}
        self.assertTrue(all(getattr(parser_args, key) == value
                            for key, value in expected_args.items()))
        argv.extend(['--show-viral'])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        expected_args['show_viral'] = True
        self.assertTrue(all(getattr(parser_args, key) == value
                            for key, value in expected_args.items()))

    def test_album(self):
        argv = ['album', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.album_id, argv[1])
        self.assertEqual(parser_args.func.__name__, 'cmd_album')
        self.assertTrue(_cli.client.get_album.called)
        self.assertRaises(SystemExit, self.cli, argv[0])

    def test_album_images(self):
        argv = ['album-images', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.album_id, argv[1])
        self.assertEqual(parser_args.output_file, None)
        self.assertEqual(parser_args.func.__name__, 'cmd_album_images')
        self.assertTrue(_cli.client.get_album_images.called)
        self.assertRaises(SystemExit, self.cli, argv[0])
        self.assertRaises(SystemExit, self.cli,
                          [argv[0], '--output-file', 'dummy.json'])

    def test_image(self):
        argv = ['image', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.image_id, argv[1])
        self.assertEqual(parser_args.func.__name__, 'cmd_image')
        self.assertTrue(_cli.client.get_image.called)
        self.assertRaises(SystemExit, self.cli, argv[0])

    def test_gallery_random(self):
        argv = ['gallery-random']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.func.__name__, 'cmd_gallery_random')
        self.assertTrue(_cli.client.gallery_random.called)
        self.assertEqual(parser_args.page, 0)
        self.assertEqual(parser_args.output_file, None)
        argv.extend(['--page', '12', '--output-file', 'dummy.json'])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertEqual(parser_args.page, int(argv[2]))
        self.assertEqual(parser_args.output_file, argv[4])
        self.assertTrue(isinstance(parser_args.page, int))

    def test_gallery_tag(self):
        argv = ['gallery-tag', 'dogs']
        self._client.return_value.gallery_tag.return_value = mock.Mock(items=[])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.func.__name__, 'cmd_gallery_tag')
        self.assertTrue(_cli.client.gallery_tag.called)
        self.assertRaises(SystemExit, self.cli, argv[0])
        expected_args = {'tag': argv[1], 'sort': 'viral', 'page': 0,
                         'window': 'week', 'output_file': None}
        self.assertTrue(all(getattr(parser_args, key) == value
                            for key, value in expected_args.items()))

    def test_gallery_tag_image(self):
        argv = ['gallery-tag-image', 'dogs', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.tag, argv[1])
        self.assertEqual(parser_args.image_id, argv[2])
        self.assertEqual(parser_args.func.__name__, 'cmd_gallery_tag_image')
        self.assertTrue(_cli.client.gallery_tag_image.called)
        self.assertRaises(SystemExit, self.cli, argv[0])
        self.assertRaises(SystemExit, self.cli, argv[:2])

    def test_gallery_item_tags(self):
        argv = ['gallery-item-tags', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(argv[0] in _cli.subcommands)
        self.assertEqual(parser_args.item_id, argv[1])
        self.assertEqual(parser_args.func.__name__, 'cmd_gallery_item_tags')
        self.assertTrue(_cli.client.gallery_item_tags.called)
        self.assertRaises(SystemExit, self.cli, argv[0])
