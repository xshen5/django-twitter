from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FriendshipPagination(PageNumberPagination):
    # set default page size, when there's no page params in request
    page_size = 20
    # default page_size_query_param is None, which means client cannot sepecify the page size
    # adding the following line will allow client to specify a page size using parameter
    # size = 10,
    # between Mobile and Desktop the page size could be different
    page_size_query_param = 'size'
    # setup allowed max page_size
    max_page_size = 20


    def get_paginated_response(self, data):
        return Response({
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'has_next_page': self.page.has_next(),
            'results': data,
        })