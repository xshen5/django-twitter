from rest_framework.response import Response
from rest_framework import status
from functools import wraps


def required_params(request_attr='query_params', params=None):
    """

    """
    if params is None:
        params = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            data = getattr(request, request_attr)
            missing_parameters = [
                param
                for param in params
                if param not in data
            ]
            if missing_parameters:
                params_str = ','.join(missing_parameters)
                return Response({
                    'message': u'missing {} in request'.format(params_str),
                    'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)
            return view_func(instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator