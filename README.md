# imgur-cli

A command line interface for Imgur

## Requirements
- Python 3
- imgurpython (>= 1.1.6)
- pip - instructions [here](https://pip.pypa.io/en/latest/installing.html)
- virtualenvwrapper - instructions [here](https://virtualenvwrapper.readthedocs.org/en/latest/install.html) (can also use [virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html))

For tests, additional requirements:

- testtools
- nose
- coverage

## Installation

    pip install imgurpython


## Imgur API Documentation


Documentation for the Imgur API can be found [here](https://api.imgur.com/).

## Authentication

You must [register](http://api.imgur.com/oauth2/addclient) the CLI with the Imgur API, and provide the Client-ID to make *any* request to the API (see the [Authentication](https://api.imgur.com/#authentication) note). If you want to perform actions as a user, the user will have to authorize your CLI through OAuth2.

To use the CLI from a strictly anonymous context (no actions on behalf of a user), you need only the client id and client secret. Once you have these, you need to set them up as environment variables. 

    export IMGUR_CLIENT_ID=<IMGUR_CLIENT_ID>
    export IMGUR_CLIENT_SECRET=<IMGUR_CLIENT_SECRET>


To take actions as a logged in user, you will additionally need an access token and refresh token. You can use the Imgur CLI to do the following:

1. Get authorization url:
    
    ```
    imgur auth url
    ```
    
2. Go to authorization url to retrieve PIN and then run the following command:

    ```
    imgur auth set-user-auth <pin>
    ```
    
3. Even though Imgur will set the access token and refresh token, you should also set them as environment variables. After running the command from (2), you will receive the access token and the refresh token. You can set them as follows:

    export IMGUR_ACCESS_TOKEN=<IMGUR_ACCESS_TOKEN>
    export IMGUR_REFRESH_TOKEN=<IMGUR_REFRESH_TOKEN>

## Library Usage

### Help

Run ```imgur help``` to see available subparsers:

    imgur help

**Output**

    imgur help
    usage: imgur [-h] [-v] <subparsers> ...

    Imgur CLI

    positional arguments:
      <subparsers>
      help         Display help about this program or one        of its subparsers
      gallery      Gallery subparser
      image        Image subparser
      notification
                   Notification subparser
      memegen      Memegen subparser
      auth         Authentication subparser
      comment      Comment subparser
      conversation
                   Conversation subparser
      account      Account subparser
      album        Album subparser

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  show program's version number and exit

    See "imgur help <SUBPARSER> <SUBCOMMAND>" for help on   a specific subparser or subcommand

For help on each subparser, you can run:

    imgur help <subparser>
    
For help of each subcommandm you can run:

    imgur help <subparser> <subcommand>

### Examples

#### Gallery Items

    imgur gallery items

**Sample output**

    {
    "gallery": [
        {
            "layout": "blog",
            "cover_height": 360,
            "account_id": 147142,
            "id": "AzrRs",
            "cover": "gW3whO8",
            "is_album": true,
            "comment_count": 184,
            "title": "5 Salads with More Calories Than a Big Mac",
            "section": "",
            "topic_id": 11,
            "downs": 279,
            "nsfw": false,
            "link": "http://imgur.com/a/AzrRs",
            "account_url": "Housemaster",
            "topic": "The More You Know",
            "comment_preview": null,
            "score": 6999,
            "images_count": 6,
            "cover_width": 640,
            "ups": 7282,
            "favorite": false,
            "views": 109548,
            "privacy": "hidden",
            "datetime": 1446568913,
            "points": 7003,
            "description": null,
            "vote": null
        },
        {
            "layout": "blog",
            "cover_height": 3264,
            "account_id": null,
            "id": "Oz5SW",
            "cover": "lJJZVRv",
            "is_album": true,
            "comment_count": 264,
            "title": "It has never been harder to leave my apartment",
            "section": "pics",
            "topic_id": 0,
            "downs": 171,
            "nsfw": false,
            "link": "http://imgur.com/a/Oz5SW",
            "account_url": null,
            "topic": null,
            "comment_preview": null,
            "score": 12858,
            "images_count": 3,
            "cover_width": 2448,
            "ups": 12070,
            "favorite": false,
            "views": 1058140,
            "privacy": "public",
            "datetime": 1446555875,
            "points": 11899,
            "description": null,
            "vote": null
        }
        ...
      ]
    }


#### Gallery Items with different arguments

    imgur gallery items --section hot --sort top --page 2 
    
#### Save output of gallery items to a file

Some commands allow to store output in a file (you run the -h option with each command to check). 

    imgur gallery items --output-file <path_to_file>

## Author

Usman Ehtesham Gul (ueg1990) - <uehtesham90@gmail.com> 

## Contribute

If you want to add any new features, or improve existing ones, feel free to send a pull request. If you have any questions or need help/mentoring with contributions, feel free to contact via email

