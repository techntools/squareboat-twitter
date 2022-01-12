from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        if isinstance(exc.detail, list):
            response.data = { 'message': '. '.join([e for e in exc.detail]) }
        else:
            fields = response.data

            response.data = {}
            response.data['fields'] = {
                **fields
            }

            messages = []
            for k, v in fields.items():
                for m in v:
                    messages.append(m)

            response.data["message"] = ' '.join(messages)

        response.data["error"] = True
    elif response is not None:
        response.data["message"] = str(exc)
        response.data["error"] = True

    if response and 'detail' in response.data:
        del response.data["detail"]

    return response
