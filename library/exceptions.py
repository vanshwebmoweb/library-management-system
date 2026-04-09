from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code
        error_message = response.data

        view = context.get('view', None)
        view_name = view.__class__.__name__ if view else None


        custom_response = {
            'status': 'error',
            'code': status_code,
            'message': error_message,
            'view': view_name,
        }

        response.data = custom_response

    return response