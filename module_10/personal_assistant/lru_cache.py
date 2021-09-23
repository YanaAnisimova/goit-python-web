import copy
from datetime import datetime
import json
import redis
from bson.objectid import ObjectId

# Работает только на поиск, при изменении данных в db данные в кеше автоматически не меняются!!!

redis_db = redis.Redis(
    host='localhost',
    port=6379,
    db=1
)


class LruCache:
    def __init__(self, func, max_size):
        self.func = func
        self.max_size = max_size
        self.key_list = 'cache_queue'

    def __call__(self, *args, **kwargs):
        # redis_db.flushdb()
        cache_key = self._convert_call_arguments_to_hash(self.func, args, kwargs)
        value_cache_key = redis_db.get(cache_key)
        if value_cache_key:
            result_json = value_cache_key
            result = self._unpacks_from_json(copy.deepcopy(result_json))
            print('CACHE !!!!!!')
        else:
            result = self.func(*args, **kwargs)
            result_json = self._packs_in_json(copy.deepcopy(result))
            print('DB !!!!!!!')

        self._update_cache_key_with_value(cache_key, result_json)
        self._evict_cache_if_necessary()
        print('key_list (Queue): ', redis_db.lrange(self.key_list, 0, -1))
        return result

    @staticmethod
    def _packs_in_json(data):
        res = list()
        for el in data:
            # converting ObjectId -> str
            el['_id'] = str(el['_id'])
            # converting datetime -> str
            bd = el['birthday']
            el['birthday'] = bd.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            res.append(el)

        return json.dumps(res)

    @staticmethod
    def _unpacks_from_json(data):
        unpacked_data = json.loads(data)
        result = list()

        for el in unpacked_data:
            # converting str -> datetime
            el['birthday'] = datetime.strptime(el['birthday'], "%Y-%m-%dT%H:%M:%S.000Z")
            # converting str -> ObjectId
            el['_id'] = ObjectId(el['_id'])
            result.append(el)

        return result

    def _update_cache_key_with_value(self, key, value):
        # Transaction
        pipeline = redis_db.pipeline()
        pipeline.multi()
        # Create/update str `key`
        redis_db.set(key, value)

        # Remove existing `key` from the list ("queue")
        if key.encode('utf-8') in redis_db.lrange(self.key_list, 0, -1):
            redis_db.lrem(self.key_list, 0, key)

        # Push `value` onto the head of the list ("queue")
        redis_db.lpush(self.key_list, key)
        pipeline.execute(raise_on_error=True)

    def _evict_cache_if_necessary(self):
        if redis_db.llen(self.key_list) > self.max_size:
            # Remove and return the last item of the list ("queue")
            oldest_key = redis_db.rpop(self.key_list)
            redis_db.delete(oldest_key)

    @staticmethod
    def _convert_call_arguments_to_hash(funk, args, kwargs):
        return str(funk.__name__) + str(args) + str(kwargs)


def lru_cache(max_size=5):
    def wrapper(func):
        cache = LruCache(func, max_size)
        return cache
    return wrapper






