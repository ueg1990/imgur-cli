import sys

import fixtures
import imgurpython
import testtools

import imgur_cli.cli as cli

FAKE_ENV = {'IMGUR_CLIENT_ID': 'client_id',
            'IMGUR_CLIENT_SECRET': 'client_secret',
            'IMGUR_ACCESS_TOKEN': 'access_token',
            'IMGUR_REFRESH_TOKEN': 'refresh_token',
            'IMGUR_MASHAPE_KEY': 'mashape_key'}


class TestImgurCli(testtools.TestCase):

    def make_env(self, exclude=None):
        if not exclude:
            exclude = []
        env = {key: value for key, value in FAKE_ENV.items() if key not in exclude}
        self.useFixture(fixtures.MonkeyPatch('os.environ', env))

    def test_imgur_credentials_env(self):
        self.make_env()
        expected = ('client_id', 'client_secret', 'access_token', 'refresh_token',
                    'mashape_key')
        imgur_credentials = cli.imgur_credentials()
        self.assertEqual(expected, imgur_credentials)
        self.make_env(exclude=['IMGUR_MASHAPE_KEY'])
        expected = ('client_id', 'client_secret', 'access_token', 'refresh_token',
                    None)
        imgur_credentials = cli.imgur_credentials()
        self.assertEqual(expected, imgur_credentials)
        self.make_env(exclude=['IMGUR_CLIENT_ID'])
        self.assertRaises(imgurpython.client.ImgurClientError,
                          cli.imgur_credentials)
        self.make_env(exclude=['IMGUR_CLIENT_SECRET'])
        self.assertRaises(imgurpython.client.ImgurClientError,
                          cli.imgur_credentials)
