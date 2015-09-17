import argparse
import logging
import os

import imgurpython

from collections import namedtuple

logger = logging.getLogger(__name__)

def imgur_credentials():
    ImgurCredentials = namedtuple('ImgurCredentials', ['client_id', 'client_secret', 'access_token', 'refresh_token', 'mashape_key'])
    try:
        from config import config
        client_id = config.get('IMGUR_CLIENT_ID')
        client_secret = config.get('IMGUR_CLIENT_SECRET')
        access_token = config.get('IMGUR_ACCESS_TOKEN')
        refresh_token = config.get('IMGUR_REFRESH_TOKEN')
        mashape_key = config.get('IMGUR_MASHAPE_KEY')
    except ImportError:
        client_id = os.environ.get('IMGUR_CLIENT_ID')
        client_secret = os.environ.get('IMGUR_CLIENT_SECRET')
        access_token = os.environ.get('IMGUR_ACCESS_TOKEN')
        refresh_token = os.environ.get('IMGUR_REFRESH_TOKEN')
        mashape_key = os.environ.get('IMGUR_MASHAPE_KEY')
    if not client_id or not client_secret:
        raise imgurpython.client.ImgurClientError('Client credentials not found. Ensure you have both client id and client secret')    
    return ImgurCredentials(client_id, client_secret, access_token, refresh_token, mashape_key)
