from rest_framework.renderers import JSONRenderer


class ResponseJSONRenderer(JSONRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        if data is None:
            return

        if 'error' in data:
            resp = data
            del resp['error']
        elif isinstance(data, str):
            resp = {
                'message': data,
            }
        else:
            resp = {
                'data': data,
            }

            if 'results' in data:
                resp['data'] = data['results']

            if 'metadata' in data:
                resp['metadata'] = data['metadata']

            if 'password' in resp['data']:
                del resp['data']['password']

        response = super().render(resp)

        return response
