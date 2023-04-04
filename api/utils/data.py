from rest_framework.pagination import PageNumberPagination


class ModifyPage(PageNumberPagination):
    page_size= 10000
    page_query_param='p'   
    page_size_query_param='page_size'   
    max_page_size= 30      
    last_page_strings='end'