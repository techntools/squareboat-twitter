from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ListPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        resp = {
            'metadata': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total': self.count,
            },
            'results': data
        }

        return Response(resp)
