import imgurpython

from imgur_cli import exceptions
from imgur_cli.utils import (cli_arg, cli_subparser, data_fields, generate_output,
                             format_comment_tree)
from imgur_cli.utils import cli_subparser
from imgur_cli.utils import data_fields
from imgur_cli.utils import generate_output


SUBPARSERS = {'gallery': 'Gallery subparser', 'album': 'Album subparser',
              'image': 'Image subparser', 'comment': 'Comment subparser',
              'memegen': 'Memegen subparser', 'account': 'Account subparser',
              'custom-gallery': 'Custom Gallery subparser',
              'conversation': 'Conversation subparser',
              'notification': 'Notification subparser'}


@cli_subparser('account')
@cli_arg('username', help='Username of Account')
def cmd_account_user(client, args):
    """
    Request standard user information. If you need the username for the account
    that is logged in, it is returned in the request for an access token
    """
    account_user = client.get_account(args.username)
    data = account_user.__dict__
    generate_output({'account_user': data})


@cli_subparser('account')
@cli_arg('username', help='Username of Account')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_account_gallery_favorites(client, args):
    """Return the images the user has favorited in the gallery"""
    gallery_favorites = client.get_gallery_favorites(args.username)
    data = [item.__dict__ for item in gallery_favorites]
    generate_output({'gallery_favorites': data}, args.output_file)


@cli_subparser('account')
@cli_arg('username', help='Username of Account')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_account_favorites(client, args):
    """
    Returns the users favorited images, only accessible if you're logged
    in as the user
    """
    account_favorites = client.get_account_favorites(args.username)
    data = [item.__dict__ for item in account_favorites]
    generate_output({'account_favorites': data}, args.output_file)


@cli_subparser('account')
@cli_arg('username', help='Username of Account')
@cli_arg('--page', default=0, metavar='<page>', type=int,
         help='The data paging number (defaults to %(default)s)')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_account_submissions(client, args):
    """Return the images a user has submitted to the gallery"""
    account_submissions = client.get_account_submissions(args.username, args.page)
    data = [item.__dict__ for item in account_submissions]
    generate_output({'account_submissions': data}, args.output_file)


@cli_subparser('account')
@cli_arg('username', help='Username of Account')
def cmd_account_settings(client, args):
    """
    Returns the account settings, only accessible if you're logged
    in as the user
    """
    account_settings = client.get_account_settings(args.username)
    data = account_settings.__dict__
    generate_output({'account_settings': data})


@cli_subparser('album')
@cli_arg('album_id', help='Album ID')
def cmd_album_id(client, args):
    """Get information about a specific album"""
    album = client.get_album(args.album_id)
    data = album.__dict__
    generate_output({'album': data})


@cli_subparser('album')
@cli_arg('album_id', help='Album ID')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_album_images(client, args):
    """Return all of the images in the album"""
    album_images = client.get_album_images(args.album_id)
    data = [item.__dict__ for item in album_images]
    generate_output({'album_images': data}, args.output_file)


@cli_subparser('album')
@cli_arg('--ids', metavar='<ids>', help='Comma separated list of image ids that you '
         'want to be included in the album; you have to be logged in as the user '
         'for adding the image ids')
@cli_arg('--title', metavar='<title>', help='The title of the album')
@cli_arg('--description', metavar='<description>',
         help='The description of the album')
@cli_arg('--privacy', metavar='<privacy>', choices=['public', 'hidden', 'secret'],
         help="Sets the privacy level of the album."
              "Values are : public | hidden | secret."
              "Defaults to user's privacy settings for logged in users")
@cli_arg('--layout', metavar='<layout>',
         choices=['blog', 'grid', 'horizontal', 'vertical'],
         help='Sets the layout to display the album. '
         'Values are : blog | grid | horizontal | vertical')
@cli_arg('--cover', metavar='<cover>',
         help='The ID of an image that you want to be the cover of the album; '
         'you have to be logged in as the user')
def cmd_album_create(client, args):
    """
    Create a new album. Optional parameter of ids is an array of image ids to
    add to the album; you have to be logged in as the user for adding the image ids.

    This method is available without authenticating an account, and may be used
    merely by sending "Authorization: Client-ID {client_id}" in the request headers.
    Doing so will create an anonymous album which is not tied to an account
    """
    fields = data_fields(args, client.allowed_album_fields)
    album = client.create_album(fields)
    generate_output({'album': album})


@cli_subparser('album')
@cli_arg('album_id', help='Album ID')
@cli_arg('--ids', metavar='<ids>', help='Comma separated list of image ids that you '
         'want to be included in the album; you have to be logged in as the user '
         'for adding the image ids')
@cli_arg('--title', metavar='<title>', help='The title of the album')
@cli_arg('--description', metavar='<description>',
         help='The description of the album')
@cli_arg('--privacy', metavar='<privacy>', choices=['public', 'hidden', 'secret'],
         help="Sets the privacy level of the album."
              "Values are : public | hidden | secret."
              "Defaults to user's privacy settings for logged in users")
@cli_arg('--layout', metavar='<layout>',
         choices=['blog', 'grid', 'horizontal', 'vertical'],
         help='Sets the layout to display the album. '
         'Values are : blog | grid | horizontal | vertical')
@cli_arg('--cover', metavar='<cover>',
         help='The ID of an image that you want to be the cover of the album; '
         'you have to be logged in as the user')
def cmd_album_update(client, args):
    """
    Update the information of an album. For anonymous albums, {album} should be the
    deletehash that is returned at creation
    """
    fields = data_fields(args, client.allowed_album_fields)
    album = client.update_album(args.album_id, fields)
    generate_output({'album': album})


@cli_subparser('album')
@cli_arg('album_id', help='Album ID')
def cmd_album_delete(client, args):
    """
    Delete an album with a given ID. You are required to be logged in as the user
    to delete the album. For anonymous albums, {album} should be the deletehash
    that is returned at creation
    """
    delete_album = client.album_delete(args.album_id)
    generate_output({'delete_album': delete_album})


@cli_subparser('album')
@cli_arg('album_id', help='Album ID')
def cmd_album_favorite(client, args):
    """
    Favorite an album with a given ID. The user is required to be logged in to
    favorite the album
    """
    favorite_album = client.album_favorite(args.album_id)
    generate_output({'favorite_album': favorite_album})


@cli_subparser('album')
@cli_arg('album_id', help='Album ID')
@cli_arg('ids', help='Comma separated list of image ids that you want to be added '
         'to the album')
def cmd_album_set_images(client, args):
    """
    Sets the images for an album, removes all other images and only uses the images
    in this request. For anonymous albums, {album} should be the deletehash that
    is returned at creation
    """
    set_images = client.album_set_images(args.album_id, args.ids)
    generate_output({'set_images': set_images})


@cli_subparser('album')
@cli_arg('album_id', help='Album ID')
@cli_arg('ids', help='Comma separated list of image ids that you want to be added '
         'to the album')
def cmd_album_add_images(client, args):
    """
    Add images for an album from a given comma separated list of image ids.
    For anonymous albums, {album} should be the deletehash that is returned
    at creation
    """
    add_images = client.album_add_images(args.album_id, args.ids)
    generate_output({'add_images': add_images})


@cli_subparser('album')
@cli_arg('album_id', help='Album ID')
@cli_arg('ids', help='Comma separated list of image ids that you want to be removed '
         'to the album')
def cmd_album_remove_images(client, args):
    """
    Remove images for an album from a given comma separated list of image ids.
    For anonymous albums, {album} should be the deletehash that is returned
    at creation
    """
    remove_images = client.album_remove_images(args.album_id, args.ids)
    generate_output({'remove_images': remove_images})


@cli_subparser('gallery')
@cli_arg('--section', default='hot', metavar='<section>',
         choices=['hot', 'top', 'user'],
         help='hot | top | user - defaults to hot')
@cli_arg('--sort', default='viral', metavar='<sort>',
         choices=['viral', 'top', 'time', 'rising'],
         help='viral | top | time | rising (only available with user section) - '
         'defaults to viral')
@cli_arg('--page', default=0, metavar='<page>', type=int,
         help='The data paging number (defaults to %(default)s)')
@cli_arg('--window', default='day', metavar='<window>',
         choices=['day', 'week', 'month', 'year', 'all'],
         help='Change the date range of the request if the section is "top", '
         'day | week | month | year | all (Defaults to %(default)s)')
@cli_arg('--show-viral', action='store_true', help='Show or hide viral images '
         'from the "user" section (Defaults to %(default)s)')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_gallery_items(client, args):
    """View items in the gallery"""
    gallery = client.gallery(args.section, args.sort, args.page, args.window,
                             args.show_viral)
    data = [item.__dict__ for item in gallery]
    generate_output({'gallery': data}, args.output_file)


@cli_subparser('gallery')
@cli_arg('tag', help='The name of the tag')
@cli_arg('--sort', default='viral', metavar='<sort>',
         choices=['viral', 'top', 'time'],
         help='viral | top | time - defaults to %(default)s')
@cli_arg('--page', default=0, metavar='<page>', type=int,
         help='The data paging number (defaults to %(default)s)')
@cli_arg('--window', default='week', metavar='<window>',
         choices=['day', 'week', 'month', 'year', 'all'],
         help='Change the date range of the request if the sort is "top", '
         'day | week | month | year | all (Defaults to %(default)s)')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_gallery_tag(client, args):
    """View images for a gallery tag"""
    gallery_tag = client.gallery_tag(args.tag, args.sort, args.page, args.window)
    data = gallery_tag.__dict__
    data['items'] = [item.__dict__ for item in data['items']]
    generate_output({'gallery_tag': data})


@cli_subparser('gallery')
@cli_arg('tag', help='The name of the tag')
@cli_arg('image_id', help='Image ID')
def cmd_gallery_tag_image(client, args):
    """View a single image in a gallery tag"""
    gallery_tag_image = client.gallery_tag_image(args.tag, args.image_id)
    data = gallery_tag_image.__dict__
    generate_output({'gallery_tag_image': data})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_item_tags(client, args):
    """View tags for a gallery item"""
    gallery_item_tags = client.gallery_item_tags(args.item_id)
    data = [item.__dict__ for item in gallery_item_tags]
    generate_output({'gallery_item_tags': data})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
@cli_arg('tag', help='The name of the tag')
@cli_arg('vote', choices=['up', 'down'], help="'up' or 'down'")
def cmd_gallery_tag_vote(client, args):
    """
    Vote for a tag, 'up' or 'down' vote. Send the same value again to undo a vote
    """
    gallery_tag_vote = client.gallery_tag_vote(args.item_id, args.tag, args.vote)
    generate_output({'gallery_tag_vote': gallery_tag_vote})


@cli_subparser('gallery')
@cli_arg('--page', default=0, metavar='<page>', type=int,
         help='A page of random gallery images, from 0-50. '
         'Pages are regenerated every hour (defaults to %(default)s)')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_gallery_random(client, args):
    """View a random set of gallery items"""
    gallery_random = client.gallery_random(args.page)
    data = [item.__dict__ for item in gallery_random]
    generate_output({'gallery_random': data}, args.output_file)


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
@cli_arg('title', help='The title of the image')
@cli_arg('--terms', default=0, type=int, metavar='<terms>',
         help='If the user has not accepted our terms yet, this endpoint will '
         'return an error. To by-pass the terms in general simply set this '
         'value to 1')
def cmd_gallery_publish(client, args):
    """Share an Album or Image to the Imgur Gallery"""
    publish_to_imgur = client.share_on_imgur(args.item_id, args.title, args.terms)
    generate_output({'publish_to_imgur': publish_to_imgur})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_remove(client, args):
    """
    Remove an item from the gallery. You must be logged in as the owner of the
    item to do this action
    """
    gallery_remove = client.remove_from_gallery(args.item_id)
    generate_output({'gallery_remove': gallery_remove})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_item(client, args):
    """View item in a gallery"""
    gallery_item = client.gallery_item(args.item_id)
    data = gallery_item.__dict__
    generate_output({'gallery_item': data})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_report(client, args):
    """Report an item in the gallery"""
    report_gallery_item = client.report_gallery_item(args.item_id)
    generate_output({'report_gallery_item': report_gallery_item})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
@cli_arg('--vote', default='up', metavar='<vote>', choices=['up', 'down'],
         help="'up' or 'down'")
def cmd_gallery_item_vote(client, args):
    """
    Vote for an item in the gallery, 'up' or 'down' vote. Send the same value
    again to undo a vote
    """
    gallery_item_vote = client.gallery_item_vote(args.item_id, args.vote)
    generate_output({'gallery_item_vote': gallery_item_vote})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
@cli_arg('--sort', default='best', metavar='<sort>', choices=['best', 'top', 'new'],
         help='best | top | new - defaults to %(default)s')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_gallery_comments(client, args):
    """Get comments on an item in the gallery"""
    gallery_comments = client.gallery_item_comments(args.item_id, args.sort)
    data = format_comment_tree(gallery_comments)
    generate_output({'gallery_comments': data}, args.output_file)


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
@cli_arg('comment', help='The text of the comment')
def cmd_gallery_create_comment(client, args):
    create_comment = client.gallery_comment(args.item_id, args.comment)
    generate_output({'create_comment': create_comment})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_comment_ids(client, args):
    """List all of the IDs for the comments on an item in the gallery"""
    gallery_comment_ids = client.gallery_comment_ids(args.item_id)
    generate_output({'gallery_comment_ids': gallery_comment_ids})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_comment_count(client, args):
    """The number of comments on an item in the gallery"""
    gallery_comment_count = client.gallery_comment_count(args.item_id)
    generate_output({'gallery_comment_count': gallery_comment_count})


@cli_subparser('image')
@cli_arg('image_id', help='Image ID')
def cmd_image_id(client, args):
    """Get information about an image"""
    image = client.get_image(args.image_id)
    data = image.__dict__
    generate_output({'image': data})


@cli_subparser('image')
@cli_arg('type', choices=['file', 'url'],
         help="The type of the file that's being sent; file, base64 or URL")
@cli_arg('image', help='A binary file, base64 data, or a URL for an image '
                       '(up to 10MB)')
@cli_arg('--name', metavar='<name>', help='The name of the file, '
         'this is automatically detected if uploading a file with a POST and '
         'multipart / form-data')
@cli_arg('--title', metavar='<title>', help='The title of the image')
@cli_arg('--album', metavar='<album>',
         help='The id of the album you want to add the image to')
@cli_arg('--description', metavar='<description>',
         help='The description of the image')
def cmd_image_upload(client, args):
    """Upload a new image"""
    config = data_fields(args, client.allowed_image_fields)
    if args.type == 'file':
        image = client.upload_from_path(args.image, config)
    else:
        image = client.upload_from_url(args.image, config)
    generate_output({'image': image})


@cli_subparser('image')
@cli_arg('image_id', help='Image ID')
def cmd_image_delete(client, args):
    """
    Deletes an image. For an anonymous image, {id} must be the image's deletehash.
    If the image belongs to your account then passing the ID of the image is
    sufficient
    """
    image_to_delete = client.delete_image(args.image_id)
    generate_output({'deleted': image_to_delete})


@cli_subparser('image')
@cli_arg('image_id', help='Image ID')
def cmd_image_favorite(client, args):
    """
    Favorite an image with a given ID. The user is required to be logged in to
    favorite the image
    """
    favorite_image = client.favorite_image(args.image_id)
    generate_output({'favorite_image': favorite_image})


@cli_subparser('conversation')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_conversation_list(client, args):
    """Get list of all conversations for the logged in user"""
    conversation_list = client.conversation_list()
    data = [item.__dict__ for item in conversation_list]
    generate_output({'conversation_list': data}, args.output_file)


@cli_subparser('conversation')
@cli_arg('conversation_id', type=int, help='Conversation ID')
@cli_arg('--page', default=1, metavar='<page>', type=int,
         help='Page of message thread. Starting at 1 for the most recent 25 '
         'messages and counting upwards (defaults to %(default)s)')
@cli_arg('--offset', default=0, metavar='<offset>', type=int,
         help='Additional offset in current page (defaults to %(default)s)')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_conversation_id(client, args):
    """Get information about a specific conversation. Includes messages"""
    conversation = client.get_conversation(args.conversation_id,
                                           args.page, args.offset)
    data = conversation.__dict__
    try:
        data['messages'] = [item.__dict__ for item in data['messages']]
    except TypeError:
        pass
    generate_output({'conversation': data})


@cli_subparser('conversation')
@cli_arg('recipient', help='The recipient username, this person will receive '
         'the message')
@cli_arg('body', help='The message body')
def cmd_conversation_create(client, args):
    """Create a new message"""
    create_message = client.create_message(args.recipient, args.body)
    generate_output({'create_message': create_message})


@cli_subparser('conversation')
@cli_arg('conversation_id', type=int, help='Conversation ID')
def cmd_conversation_delete(client, args):
    """Delete a conversation by the given ID"""
    delete_conversation = client.delete_conversation(args.conversation_id)
    generate_output({'delete_conversation': delete_conversation})


@cli_subparser('conversation')
@cli_arg('username', help='Username of sender to report')
def cmd_conversation_report(client, args):
    """Report a user for sending messages that are against the Terms of Service"""
    report_sender = client.report_sender(args.username)
    generate_output({'report_sender': report_sender})


@cli_subparser('conversation')
@cli_arg('username', help='Username of sender to block')
def cmd_conversation_block(client, args):
    """Block the user from sending messages to the user that is logged in"""
    block_sender = client.block_sender(args.username)
    generate_output({'block_sender': block_sender})


@cli_subparser('notification')
@cli_arg('--new', default=True, metavar='<new>', choices=[True, False], type=bool,
         help='boolean - false for all notifications, true for only non-viewed '
         'notification (defaults to %(default)s)')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_notification_all(client, args):
    """Get all notifications for the user that's currently logged in"""
    notifications_all = client.get_notifications(args.new)
    notifications_all['messages'] = [message.__dict__ for message in
                                     notifications_all['messages']]
    formatted_replies = []
    for reply in notifications_all['replies']:
        formatted_reply = reply.__dict__
        formatted_reply['content'] = format_comment_tree(formatted_reply['content'])
        formatted_replies.append(formatted_reply)
    notifications_all['replies'] = formatted_replies
    generate_output({'notifications_all': notifications_all}, args.output_file)


@cli_subparser('notification')
@cli_arg('notification_id', type=int, help='Notification ID')
def cmd_notification_id(client, args):
    """Returns the data about a specific notification"""
    notification = client.get_notification(args.notification_id)
    notification = notification.__dict__
    if 'comment' in notification['content']:
        notification['content'] = format_comment_tree(notification['content'])
    generate_output({'notification': notification})


@cli_subparser('notification')
@cli_arg('ids', help='Comma separated list of notification ids to mark as viewed')
def cmd_notification_mark(client, args):
    """
    Marks a notification  or multiple notifications as viewed, this way it no
    longer shows up in the basic notification request
    """
    # Converted to list because in current implemented in imgurpython, client method
    # expected a comma separated list of ids
    ids = args.ids.split(',')
    notifications_marked_as_viewed = client.mark_notifications_as_read(args.ids)
    generate_output({'notifications_marked_as_viewed':
                     notifications_marked_as_viewed})


@cli_subparser('comment')
@cli_arg('comment_id', type=int, help='Comment ID')
def cmd_comment_id(client, args):
    """Get information about a specific comment"""
    comment = client.get_comment(args.comment_id)
    data = comment.__dict__
    generate_output({'comment': data})


@cli_subparser('comment')
@cli_arg('comment_id', type=int, help='Comment ID')
def cmd_comment_delete(client, args):
    """Delete a comment by the given id"""
    delete_comment = client.delete_comment(args.comment_id)
    generate_output({'delete_comment': delete_comment})


@cli_subparser('comment')
@cli_arg('comment_id', type=int, help='Comment ID')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_comment_replies(client, args):
    """Get the comment with all of the replies for the comment"""
    comment_replies = client.get_comment_replies(args.comment_id)
    data = format_comment_tree(comment_replies)
    generate_output({'comment_replies': data}, args.output_file)


@cli_subparser('comment')
@cli_arg('comment_id', type=int, help='Comment ID')
@cli_arg('image_id', help='Image ID')
@cli_arg('comment', help='The comment text, this is what will be displayed')
def cmd_comment_reply(client, args):
    """Create a reply for the given comment"""
    comment_reply = client.post_comment_reply(args.comment_id, args.image_id,
                                              args.comment)
    generate_output({'comment_reply': comment_reply})


@cli_subparser('comment')
@cli_arg('comment_id', type=int, help='Comment ID')
@cli_arg('--vote', default='up', metavar='<vote>', choices=['up', 'down'],
         help="'up' or 'down'")
def cmd_comment_vote(client, args):
    """Vote on a comment. The {vote} variable can only be set as "up" or "down"""
    comment_vote = client.comment_vote(args.comment_id, args.vote)
    generate_output({'comment_vote': comment_vote})


@cli_subparser('comment')
@cli_arg('comment_id', type=int, help='Comment ID')
def cmd_comment_report(client, args):
    """Report a comment for being inappropriate"""
    comment_report = client.comment_report(args.comment_id)
    generate_output({'comment_report': comment_report})


@cli_subparser('memegen')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_memegen_default_memes(client, args):
    """Get the list of default memes"""
    default_memes = client.default_memes()
    data = [item.__dict__ for item in default_memes]
    generate_output({'default_memes': args.output_file})
