# -*- coding:UTF-8 -*-
from django.core.cache import cache

from common import rds
from common.keys import PAGE_KEY, READ_COUNT


def page_cache(timeout):
    '''
            # 缓存更新
            # 1.手动更新
            # 2.删除旧缓存
            # 3.通过过期时间自动更新
            :param view_func:
            :return:
    '''
    def wrap1(view_func):
        def wrap(request,*args,**kwargs):
            key = PAGE_KEY % request.get_full_path()
            print('&&&&&&&&&&&&',key)
            response = cache.get(key)

            print('get response from cache:', response)
            if response is None:
                response = view_func(request,*args,**kwargs)
                cache.set(key,response,timeout)
                print('set response from view:', response)
            return response
        return wrap
    return wrap1



def read_count(read_view):
    def wrap(request):
        post_id = int(request.GET.get('post_id',1))
        a = rds.zincrby(READ_COUNT,post_id)
        print('**********',a)
        return read_view(request)
    return wrap








