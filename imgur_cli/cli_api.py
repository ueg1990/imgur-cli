import imgurpython

from imgur_cli import exceptions
from imgur_cli.utils import cli_arg
from imgur_cli.utils import cli_subparser
from imgur_cli.utils import data_fields
from imgur_cli.utils import generate_output


SUBPARSERS = {'gallery': 'Gallery subparser', 'album': 'Album subparser',
              'image': 'Image subparser', 'comment': 'Comment subparser'}


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
@cli_arg('--vote', default='up', choices=['up', 'down'], help="'up' or 'down'")
def cmd_gallery_item_vote(client, args):
    """
    Vote for an image, 'up' or 'down' vote. Send the same value again to undo a vote
    """
    gallery_item_vote = client.gallery_item_vote(args.item_id, args.vote)
    generate_output({'gallery_item_vote': gallery_item_vote})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_comment_ids(client, args):
    """List all of the IDs for the comments on an image"""
    gallery_comment_ids = client.gallery_comment_ids(args.item_id)
    generate_output({'gallery_comment_ids': gallery_comment_ids})


@cli_subparser('gallery')
@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_comment_count(client, args):
    """List all of the IDs for the comments on an image"""
    gallery_comment_count = client.gallery_comment_count(args.item_id)
    generate_output({'gallery_comment_count': gallery_comment_count})


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
@cli_arg('album_id', help='Album ID')
@cli_arg('image_id', help='Image ID')
def cmd_album_image(client, args):
    """
    Get information about an image in an album -
    Not implemented yet in imgurpython
    """
    raise exceptions.CommandError('Not implemented yet in imgurpython')


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
@cli_arg('--title', metavar='<title>', help='The title of the album')
@cli_arg('--description', metavar='<description>')
def cmd_image_update(client, args):
    """
    Updates the title or description of an image. You can only update an image
    you own and is associated with your account. For an anonymous image,
    {id} must be the image's deletehash -  Not implemented yet in imgurpython
    """
    raise exceptions.CommandError('Not implemented yet in imgurpython')


@cli_subparser('image')
@cli_arg('image_id', help='Image ID')
def cmd_image_favorite(client, args):
    """
    Favorite an image with a given ID. The user is required to be logged in to
    favorite the image
    """
    favorite_image = client.favorite_image(args.image_id)
    generate_output({'favorite_image': favorite_image})


@cli_subparser('comment')
@cli_arg('comment_id', help='Comment ID')
def cmd_comment_id(client, args):
    """Get information about a specific comment"""
    try:
        comment = client.get_comment(int(args.comment_id))
        data = comment.__dict__
        generate_output({'comment': data})
    except ValueError:
        raise exceptions.CommandError('Given comment id is a string; '
                                      'expecting a number')
