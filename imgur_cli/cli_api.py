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
         choices=['hot', 'top', 'user'],
         help='Change the date range of the request if the section is "top", '
         'day | week | month | year | all (Defaults to %(default)s)')
@cli_arg('--show-viral', default='False', action='store_true',
         help='Show or hide viral images from the '
         '"user" section (Defaults to %(default)s)')
def cmd_gallery(client, args):
    """Returns the images in the gallery"""
    gallery = client.gallery()
    data = [item.__dict__ for item in gallery]
    generate_output(args.output_file, {'gallery': data})


@cli_arg('album_id', help='Album ID')
def cmd_album(client, args):
    """Get information about a specific album"""
    album = client.get_album(args.album_id)
    data = album.__dict__
    generate_output(args.output_file, {'album': data})


@cli_arg('album_id', help='Album ID')
def cmd_album_images(client, args):
    """Get information about a specific album"""
    album_images = client.get_album_images(args.album_id)
    data = [item.__dict__ for item in album_images]
    generate_output(args.output_file, {'album_images': data})


@cli_arg('image_id', help='Image ID')
def cmd_image(client, args):
    """Get information about an image"""
    image = client.get_image(args.image_id)
    data = image.__dict__
    generate_output(args.output_file, {'image': data})


@cli_arg('--page', default=0, metavar='<page>', type=int,
         help='A page of random gallery images, from 0-50. '
         'Pages are regenerated every hour (defaults to %(default)s)')
def cmd_gallery_random(client, args):
    """Returns a random set of gallery images"""
    gallery_random = client.gallery_random(args.page)
    data = [item.__dict__ for item in gallery_random]
    generate_output(args.output_file, {'gallery_random': data})
