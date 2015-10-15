import imgurpython

from imgur_cli.exceptions import CommandError
from imgur_cli.utils import cli_arg
from imgur_cli.utils import generate_output


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
def cmd_gallery(client, args):
    """Returns the images in the gallery"""
    gallery = client.gallery(args.section, args.sort, args.page, args.window,
                             args.show_viral)
    data = [item.__dict__ for item in gallery]
    generate_output({'gallery': data}, args.output_file)


@cli_arg('album_id', help='Album ID')
def cmd_album(client, args):
    """Get information about a specific album"""
    album = client.get_album(args.album_id)
    data = album.__dict__
    generate_output({'album': data})


@cli_arg('album_id', help='Album ID')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_album_images(client, args):
    """Get information about a specific album"""
    album_images = client.get_album_images(args.album_id)
    data = [item.__dict__ for item in album_images]
    generate_output({'album_images': data}, args.output_file)


@cli_arg('image_id', help='Image ID')
def cmd_image(client, args):
    """Get information about an image"""
    image = client.get_image(args.image_id)
    data = image.__dict__
    generate_output({'image': data})


@cli_arg('--page', default=0, metavar='<page>', type=int,
         help='A page of random gallery images, from 0-50. '
         'Pages are regenerated every hour (defaults to %(default)s)')
@cli_arg('--output-file', default=None, metavar='<output_file>',
         help='Save output to a JSON file')
def cmd_gallery_random(client, args):
    """Returns a random set of gallery images"""
    gallery_random = client.gallery_random(args.page)
    data = [item.__dict__ for item in gallery_random]
    generate_output({'gallery_random': data}, args.output_file)


@cli_arg('tag', help='The name of the tag')
@cli_arg('--sort', default='viral', metavar='<sort>',
         choices=['viral', 'top', 'time'],
         help='viral | top | time | - defaults to %(default)s')
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


@cli_arg('tag', help='The name of the tag')
@cli_arg('image_id', help='Image ID')
def cmd_gallery_tag_image(client, args):
    """View a single image in a gallery tag"""
    gallery_tag_image = client.gallery_tag_image(args.tag, args.image_id)
    data = gallery_tag_image.__dict__
    generate_output({'gallery_tag_image': data})


@cli_arg('item_id', help='Gallery item ID')
def cmd_gallery_item_tags(client, args):
    """View tags for a gallery item"""
    gallery_item_tags = client.gallery_item_tags(args.item_id)
    data = [item.__dict__ for item in gallery_item_tags]
    generate_output({'gallery_item_tags': data})
