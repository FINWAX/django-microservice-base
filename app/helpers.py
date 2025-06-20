import json
import logging
from typing import Any, Optional

from django.http import HttpRequest

logger = logging.getLogger(__name__)

def get_from_request(name: str, request: HttpRequest, default: Optional[Any] = None) -> Any:
    """
    Retrieve a parameter from a Django request.

    This function checks for the parameter in the following order of priority:
    1. JSON body (request.body)
    2. POST data (request.POST)
    3. GET data (request.GET)
    4. FILES data (request.FILES)

    :param name: The name of the parameter to retrieve.
    :type name: str
    :param request: The Django HTTP request object.
    :type request: HttpRequest
    :param default: The default value to return if the parameter is not found.
    :type default: Any, optional
    :return: The value of the parameter if found, otherwise the default value.
    :rtype: Any
    :raises json.JSONDecodeError: If the request body contains invalid JSON.
    :raises UnicodeDecodeError: If the request body cannot be decoded as UTF-8.
    """
    if request.body:
        try:
            body_params = json.loads(request.body.decode('utf-8'))
            if isinstance(body_params, dict) and name in body_params:
                return body_params[name]
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON body for parameter '{name}': {e}")
        except UnicodeDecodeError as e:
            logger.warning(f"Failed to decode request body for parameter '{name}': {e}")

    if name in request.POST:
        return request.POST[name]

    if name in request.GET:
        return request.GET[name]

    if name in request.FILES:
        return request.FILES[name]

    logger.debug(f"Parameter '{name}' not found in request, returning default: {default}")
    return default
