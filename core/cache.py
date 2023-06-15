import json
from functools import partial

from django_redis import get_redis_connection


def query_or_cache(ttl: int, alias: str, key: str, func, *args, **kwargs):
    redis_conn = get_redis_connection(alias=alias)
    if redis_conn.exists(key):
        s: str = redis_conn.get(key)
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            return s
    result = func(*args, **kwargs)
    if result:
        redis_conn.set(key, json.dumps(result, ensure_ascii=False))
        redis_conn.expire(key, ttl)
    return result


def query_or_cache_default_10min(func, key: str, *args, **kwargs):
    partial_func = partial(query_or_cache, 60 * 10, 'default')
    return partial_func(key, func, *args, **kwargs)


def query_or_cache_default(func, key: str, ttl: int, *args, **kwargs):
    partial_func = partial(query_or_cache, ttl, 'default')
    return partial_func(key, func, *args, **kwargs)
