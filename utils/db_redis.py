from django_redis import get_redis_connection


def redis_get_value(key):
    conn = get_redis_connection('default')
    res = conn.get(key)
    if res:
        return res.decode('utf-8')
    else:
        return


def redis_set_value(key, value, expire=60 * 60):
    conn = get_redis_connection('default')
    conn.set(key, value, expire)
    return

