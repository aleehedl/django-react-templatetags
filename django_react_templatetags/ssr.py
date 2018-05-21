# -*- coding: utf-8 -*-

"""
This modules manages SSR rendering logic
"""

import logging

from django.conf import settings
import requests


logger = logging.getLogger(__name__)


def load_or_empty(component):
    request_json = u'{{"componentName": "{0}", "props": {1}}}'.format(
        component['name'],
        component['json'],
    )

    inner_html = ''
    bundles = []
    try:
        data = load(request_json)
        inner_html = data.get('html', '')
        bundles = data.get('bundles', [])
    except requests.exceptions.RequestException as e:
        inner_html = ''
        logger.error(e)

    return inner_html, bundles


def load(request_json):
    req = requests.post(
        settings.REACT_RENDER_HOST,
        timeout=get_request_timeout(),
        data=request_json,
    )

    req.raise_for_status()
    return req.json()


def get_request_timeout():
    if not hasattr(settings, 'REACT_RENDER_TIMEOUT'):
        return 20

    return settings.REACT_RENDER_TIMEOUT
