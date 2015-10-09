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
