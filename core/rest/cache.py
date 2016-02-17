from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor.bits import QueryParamsKeyBit, PaginationKeyBit

class CacheKeyConstructor(DefaultKeyConstructor):
    params = QueryParamsKeyBit()
    pagination = PaginationKeyBit()