from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor import bits

class CacheKeyConstructor(DefaultKeyConstructor):
    params = bits.QueryParamsKeyBit()
    pagination = bits.PaginationKeyBit()
    args = bits.ArgsKeyBit()
    kwargs = bits.KwargsKeyBit()