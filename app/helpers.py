import json
import logging

from django.http import HttpRequest

logger = logging.getLogger(__name__)


def get_request_params(
        request: HttpRequest,
        include_get: bool = True,
        include_post: bool = True,
        include_json: bool = True,
        include_files: bool = False
) -> dict:
    """
    Creates a dictionary of parameters from a Django HTTP request.
    Parameters are included based on the provided flags and merged in the order:
    POST, JSON, GET, FILES (later sources override earlier ones).
    :param request: Django HttpRequest object
    :param include_get: Include GET parameters if True
    :param include_post: Include POST parameters if True
    :param include_json: Include JSON body parameters if True
    :param include_files: Include FILES parameters if True
    :return: Dictionary containing merged parameters
    """
    params = {}

    if include_post:
        for key, value in request.POST.items():
            params[key] = value

    if include_json and request.body:
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            if isinstance(json_data, dict):
                params.update(json_data)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error(f'Error while decoding request from json: {str(e)}')
            pass

    if include_get:
        for key, value in request.GET.items():
            params[key] = value

    if include_files:
        for key, file in request.FILES.items():
            params[key] = file

    return params
