from rest_framework.response import Response
from rest_framework import pagination


class CustomPagination(pagination.BasePagination):

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'response': data
        })
