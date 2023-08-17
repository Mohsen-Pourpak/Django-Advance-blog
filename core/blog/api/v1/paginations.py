from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class DefaultPagination(PageNumberPagination):
    page_size = 1
    def get_paginated_response(self, data):
        return Response({
            'links': {
            'next': self.get_next_link(),
            'prev': self.get_previous_link(),
            },
            'total objects': self.page.paginator.count,
            'total pages': self.page.paginator.num_pages,
            'results': data
        })