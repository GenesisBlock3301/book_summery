from rest_framework.pagination import PageNumberPagination


# Custom pagination
class CustomPagination:
    """This is custom pagination & must derive from settings.py"""
    """Custom pagination class"""
    def __init__(self):
        self.paginator = PageNumberPagination()
        
    def get_queryset(self, data, request):
        """It takes query as a parameter"""
        result_page = self.paginator.paginate_queryset(queryset=data, request=request)
        return result_page

    def get_response(self, serialized_data):
        """It takes serialized data"""
        return self.paginator.get_paginated_response(serialized_data)

