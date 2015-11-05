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

    def assertParser(self, _cli, parser_args, argv):
        """
        Assertion method for subparsers, subcommands and positional arguments.
        Parameter argv is a list where the first item is the name of the subparser,
        followed by the subcommand and the remaining items are positional arguments
        """
        number_of_parsing_levels = 2
        cmd = 'cmd_{0}_{1}'.format(argv[0], argv[1]).replace('-', '_')
        self.assertEqual(parser_args.func.__name__, cmd)
        self.assertTrue(argv[1] in _cli.subcommands)
        self.assertTrue(argv[0] in _cli.subparsers)
        number_of_positional_arguments = len(argv) - number_of_parsing_levels
        if number_of_positional_arguments:
            positional_args = []
            for item in parser_args.func.arguments:
                arg = item[0][0]
                if arg.startswith('--'):
                    break
                positional_args.append(arg)
            for index, arg in enumerate(positional_args,
                                        start=number_of_parsing_levels):
                args_type = (
                    parser_args.func.arguments[index - number_of_parsing_levels][1]
                    .get('type')
                )
                if args_type:
                    self.assertEqual(getattr(parser_args, arg),
                                     args_type(argv[index]))
                else:
                    self.assertEqual(getattr(parser_args, arg), argv[index])
                self.assertRaises(SystemExit, self.cli, argv[:index])

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

    def test_account_user(self):
        argv = ['account', 'user', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account.called)

    def test_account_gallery_favorites(self):
        argv = ['account', 'gallery-favorites', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_gallery_favorites.called)

    def test_account_favorites(self):
        argv = ['account', 'favorites', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_favorites.called)

    def test_account_submissions(self):
        argv = ['account', 'submissions', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_submissions.called)

    def test_account_settings(self):
        argv = ['account', 'settings', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_settings.called)

    def test_account_change_settings(self):
        argv = ['account', 'change-settings', 'ue90', '--username', 'ueg1990']
        self._client.return_value.allowed_account_fields = {'bio', 'public_images',
                                                            'messaging_enabled',
                                                            'album_privacy',
                                                            'accepted_gallery_terms',
                                                            'username'}
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.change_account_settings.called)
        expected_args = 'ue90', {'username': 'ueg1990'}
        _cli.client.change_account_settings.assert_called_with(*expected_args)

    def test_account_email_verification_status(self):
        argv = ['account', 'verification-status', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_email_verification_status.called)

    def test_account_send_verification_email(self):
        argv = ['account', 'send-verification', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.send_verification_email.called)

    def test_account_albums(self):
        argv = ['account', 'albums', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_albums.called)

    def test_account_album_ids(self):
        argv = ['account', 'album-ids', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_album_ids.called)

    def test_account_album_count(self):
        argv = ['account', 'album-count', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_album_count.called)

    @mock.patch('imgur_cli.cli_api.format_comment_tree')
    def test_account_comments(self, mock_format_comment_tree):
        argv = ['account', 'comments', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_comments.called)

    def test_account_comment_ids(self):
        argv = ['account', 'comment-ids', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_comment_ids.called)

    def test_account_comment_count(self):
        argv = ['account', 'comment-count', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_comment_count.called)

    def test_account_images(self):
        argv = ['account', 'images', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_images.called)

    def test_account_image_ids(self):
        argv = ['account', 'image-ids', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_image_ids.called)

    def test_account_image_count(self):
        argv = ['account', 'image-count', 'me']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_account_images_count.called)

    def test_album(self):
        argv = ['album', 'id', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_album.called)

    def test_album_images(self):
        argv = ['album', 'images', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertEqual(parser_args.output_file, None)
        self.assertTrue(_cli.client.get_album_images.called)
        self.assertRaises(SystemExit, self.cli,
                          [argv[0], '--output-file', 'dummy.json'])

    def test_album_create(self):
        argv = ['album', 'create', '--title', 'test']
        self._client.return_value.allowed_album_fields = {'ids', 'title',
                                                          'description', 'privacy',
                                                          'layout', 'cover'}
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.create_album.called)
        _cli.client.create_album.assert_called_with({'title': 'test'})

    def test_album_update(self):
        argv = ['album', 'update', '123', '--title', 'test']
        self._client.return_value.allowed_album_fields = {'ids', 'title',
                                                          'description', 'privacy',
                                                          'layout', 'cover'}
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.update_album.called)
        _cli.client.update_album.assert_called_with('123', {'title': 'test'})

    def test_album_delete(self):
        argv = ['album', 'delete', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.album_delete.called)

    def test_album_favorite(self):
        argv = ['album', 'favorite', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.album_favorite.called)

    def test_album_set_images(self):
        argv = ['album', 'set-images', '123', 'abc']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.album_set_images.called)

    def test_album_add_images(self):
        argv = ['album', 'add-images', '123', 'abc']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.album_add_images.called)

    def test_album_remove_images(self):
        argv = ['album', 'remove-images', '123', 'abc']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.album_remove_images.called)

    def test_comment_id(self):
        argv = ['comment', 'id', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_comment.called)

    def test_comment_delete(self):
        argv = ['comment', 'delete', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.delete_comment.called)

    @mock.patch('imgur_cli.cli_api.format_comment_tree')
    def test_comment_replies(self, mock_format_comment_tree):
        argv = ['comment', 'replies', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_comment_replies.called)

    def test_comment_reply(self):
        argv = ['comment', 'reply', '123', '456', 'Test comment']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.post_comment_reply.called)

    def test_comment_vote(self):
        argv = ['comment', 'vote', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.comment_vote.called)

    def test_comment_report(self):
        argv = ['comment', 'report', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.comment_report.called)

    def test_conversation_list(self):
        argv = ['conversation', 'list']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.conversation_list.called)

    def test_conversation_id_1(self):
        argv = ['conversation', 'id', '123']
        self._client.return_value.get_conversation.return_value = \
            mock.Mock(messages=[])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_conversation.called)

    def test_conversation_id_2(self):
        argv = ['conversation', 'id', '123']
        self._client.return_value.get_conversation.return_value = \
            mock.Mock(items=[])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_conversation.called)

    def test_conversation_create(self):
        argv = ['conversation', 'create', 'ue90', 'Test message']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.create_message.called)

    def test_conversation_delete(self):
        argv = ['conversation', 'delete', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.delete_conversation.called)

    def test_conversation_report(self):
        argv = ['conversation', 'report', 'ue90']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.report_sender.called)

    def test_conversation_block(self):
        argv = ['conversation', 'block', 'ue90']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.block_sender.called)

    def test_gallery(self):
        argv = ['gallery', 'items']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
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

    def test_gallery_memes_subgallery(self):
        argv = ['gallery', 'memes-subgallery']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.memes_subgallery.called)
        expected_args = {'sort': 'viral', 'page': 0, 'window': 'week',
                         'output_file': None}
        self.assertTrue(all(getattr(parser_args, key) == value
                            for key, value in expected_args.items()))

    def test_gallery_subreddit_gallery(self):
        argv = ['gallery', 'subreddit-gallery', 'soccer']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.subreddit_gallery.called)
        expected_args = {'sort': 'time', 'page': 0, 'window': 'week',
                         'output_file': None}
        self.assertTrue(all(getattr(parser_args, key) == value
                            for key, value in expected_args.items()))

    def test_gallery_subreddit_image(self):
        argv = ['gallery', 'subreddit-image', 'soccer', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.subreddit_image.called)

    def test_gallery_tag(self):
        argv = ['gallery', 'tag', 'dogs']
        self._client.return_value.gallery_tag.return_value = mock.Mock(items=[])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_tag.called)
        expected_args = {'tag': argv[2], 'sort': 'viral', 'page': 0,
                         'window': 'week', 'output_file': None}
        self.assertTrue(all(getattr(parser_args, key) == value
                            for key, value in expected_args.items()))

    def test_gallery_tag_image(self):
        argv = ['gallery', 'tag-image', 'dogs', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_tag_image.called)

    def test_gallery_item_tags(self):
        argv = ['gallery', 'item-tags', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_item_tags.called)

    def test_gallery_tag_vote(self):
        argv = ['gallery', 'tag-vote', '123', 'funny', 'up']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_tag_vote.called)
        argv[-1] = 'left'
        self.assertRaises(SystemExit, self.cli, argv)

    def test_gallery_search(self):
        argv = ['gallery', 'search', 'soccer']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_search.called)
        expected_args = {'advanced': None, 'sort': 'time', 'page': 0,
                         'window': 'all', 'output_file': None}
        self.assertTrue(all(getattr(parser_args, key) == value
                            for key, value in expected_args.items()))

    def test_gallery_random(self):
        argv = ['gallery', 'random']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_random.called)
        self.assertEqual(parser_args.page, 0)
        self.assertEqual(parser_args.output_file, None)
        argv.extend(['--page', '12', '--output-file', 'dummy.json'])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertTrue(_cli.client.gallery_random.called)
        self.assertEqual(parser_args.page, int(argv[3]))
        self.assertEqual(parser_args.output_file, argv[5])
        self.assertTrue(isinstance(parser_args.page, int))

    def test_gallery_publish(self):
        argv = ['gallery', 'publish', '123', 'Title']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.share_on_imgur.called)

    def test_gallery_remove(self):
        argv = ['gallery', 'remove', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.remove_from_gallery.called)

    def test_gallery_item(self):
        argv = ['gallery', 'item', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_item .called)

    def test_gallery_report(self):
        argv = ['gallery', 'report', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.report_gallery_item.called)

    def test_gallery_item_vote(self):
        argv = ['gallery', 'item-vote', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_item_vote.called)
        self.assertEqual(parser_args.vote, 'up')
        argv.extend(['--vote', 'down'])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertEqual(parser_args.vote, 'down')
        argv[-1] = 'left'
        self.assertRaises(SystemExit, self.cli, argv)

    @mock.patch('imgur_cli.cli_api.format_comment_tree')
    def test_gallery_comments(self, mock_format_comment_tree):
        argv = ['gallery', 'comments', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_item_comments.called)
        self.assertEqual(parser_args.sort, 'best')

    def test_gallery_create_comment(self):
        argv = ['gallery', 'create-comment', '123', 'test']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_comment.called)

    def test_gallery_comment_ids(self):
        argv = ['gallery', 'comment-ids', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_comment_ids.called)

    def test_gallery_comment_count(self):
        argv = ['gallery', 'comment-count', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.gallery_comment_count.called)

    def test_image(self):
        argv = ['image', 'id', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_image.called)

    def test_image_upload(self):
        argv = ['image', 'upload', 'file', 'test.jpg']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.upload_from_path.called)
        argv[2] = 'url'
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.upload_from_url.called)

    def test_image_delete(self):
        argv = ['image', 'delete', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.delete_image.called)

    def test_image_favorite(self):
        argv = ['image', 'favorite', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.favorite_image.called)

    def test_memegen_default_memes(self):
        argv = ['memegen', 'default-memes']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.default_memes.called)

    @mock.patch('imgur_cli.cli_api.format_comment_tree')
    def test_notification_all(self, mock_format_comment_tree):
        argv = ['notification', 'all']
        self._client.return_value.get_notifications.return_value = \
            {'messages': [mock.Mock()], 'replies': [mock.Mock(content=[])]}
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_notifications.called)

    def test_notification_id_1(self):
        argv = ['notification', 'id', '123']
        self._client.return_value.get_notification.return_value = \
            mock.Mock(content=[])
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_notification.called)

    @mock.patch('imgur_cli.cli_api.format_comment_tree')
    def test_notification_id_2(self, mock_format_comment_tree):
        argv = ['notification', 'id', '123']
        self._client.return_value.get_notification.return_value = \
            mock.Mock(content={'comment': []})
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_notification.called)

    def test_notification_mark(self):
        argv = ['notification', 'mark', '1,2,3']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.mark_notifications_as_read.called)

    def test_auth_url(self):
        argv = ['auth', 'url']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.get_auth_url.called)

    def test_auth_set_user_auth(self):
        argv = ['auth', 'set-user-auth', '123']
        _cli = self.cli(argv)
        parser_args = _cli.parser.parse_args(argv)
        self.assertParser(_cli, parser_args, argv)
        self.assertTrue(_cli.client.authorize.called)
