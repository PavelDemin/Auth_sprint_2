from functools import wraps

from app.exceptions import TooManyRequestsExceptions
from app.settings import settings
from flask import request
from pyrate_limiter import BucketFullException, Duration, Limiter, RequestRate, RedisBucket
from redis import ConnectionPool


class LimiterRequests:

    def __init__(self, rate: int = settings.LIMITER_RATE):
        self.limiter = Limiter(RequestRate(rate, Duration.SECOND),
                               bucket_class=RedisBucket,
                               bucket_kwargs={
                                   'redis_pool': ConnectionPool.from_url(url=settings.LIMITER_REDIS.DSN),
                                   'bucket_name': 'rate_limit_bucket'
                               })

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                self.limiter.try_acquire(request.remote_addr)
            except BucketFullException:
                raise TooManyRequestsExceptions('')
            return func(*args, **kwargs)

        return wrapper
