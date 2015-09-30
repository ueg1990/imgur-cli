import sys

import fixtures
import imgurpython
import testtools

from unittest import mock

import imgur_cli.cli as cli

FAKE_ENV = {'IMGUR_CLIENT_ID': 'client_id',
            'IMGUR_CLIENT_SECRET': 'client_secret',
            'IMGUR_ACCESS_TOKEN': 'access_token',
            'IMGUR_REFRESH_TOKEN': 'refresh_token',
            'IMGUR_MASHAPE_KEY': 'mashape_key'}


class TestImgurCli(testtools.TestCase):

    def make_env(self, attribute, exclude=None):
        env = {key: value for key, value in FAKE_ENV.items() if key != exclude}
        self.useFixture(fixtures.MonkeyPatch(attribute, env))

    def _test_imgur_credentials(self, attribute):
        self.make_env(attribute)
        expected = ('client_id', 'client_secret', 'access_token', 'refresh_token',
                    'mashape_key')
        imgur_credentials = cli.imgur_credentials()
        self.assertEqual(expected, imgur_credentials)
        self.make_env(attribute, exclude='IMGUR_MASHAPE_KEY')
        expected = ('client_id', 'client_secret', 'access_token', 'refresh_token',
                    None)
        imgur_credentials = cli.imgur_credentials()
        self.assertEqual(expected, imgur_credentials)
        self.make_env(attribute, exclude='IMGUR_CLIENT_ID')
        self.assertRaises(imgurpython.client.ImgurClientError,
                          cli.imgur_credentials)
        self.make_env(attribute, exclude='IMGUR_CLIENT_SECRET')
        self.assertRaises(imgurpython.client.ImgurClientError,
                          cli.imgur_credentials)

    def test_imgur_credentials_env(self):
        self.useFixture(fixtures.MonkeyPatch('imgur_cli.cli.config', None))
        self._test_imgur_credentials('os.environ')

    def test_imgur_credentials_config(self):
        self._test_imgur_credentials('imgur_cli.cli.config')
