import redis


client = redis.Redis(
    host='localhost',
    port=6379,
    db=1
)


class LruCache:
    def __init__(self, func, max_size):
        self.func = func
        self.max_size = max_size
        self.name_list = 'cache_queue'

    def __call__(self, *args, **kwargs):
        cache_key = self._convert_call_arguments_to_hash(self.func, args, kwargs)

        # if set 'cache_key' exists, takes value from set
        value_cache_key = client.get(cache_key)
        if value_cache_key:
            result = value_cache_key
        else:
            result = self.func(*args, **kwargs)

        self._update_cache_key_with_value(cache_key, result)
        self._evict_cache_if_necessary()

        print('que: ', client.lrange(self.name_list, 0, -1))
        return result

    def _update_cache_key_with_value(self, key, value):
        # Transaction
        pipeline = client.pipeline()
        pipeline.multi()
        # Create/update str `key`
        client.set(key, value)

        # Remove existing `key` from the list ("queue")
        if key in client.lrange(self.name_list, 0, -1):
            client.lrem(self.name_list, 0, key)
        # Push `value` onto the head of the list ("queue")
        client.lpush(self.name_list, key)
        pipeline.execute(raise_on_error=True)

    def _evict_cache_if_necessary(self):
        if client.llen(self.name_list) > self.max_size:
            # Remove and return the last item of the list ("queue")
            oldest_key = client.rpop(self.name_list)
            client.delete(oldest_key)

    @staticmethod
    def _convert_call_arguments_to_hash(funk, args, kwargs):
        return str(funk.__name__) + str(args) + str(kwargs)


def lru_cache(max_size=5):
    def wrapper(func):
        cache = LruCache(func, max_size)
        return cache
    return wrapper


@lru_cache()
def foo(value: str):

    return f'result_{value}'


if __name__ == '__main__':
    client.flushdb()

    for i in 'ABACBDEG':
        foo(i)

    # "GEDBC"

