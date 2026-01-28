from fastapi import Request, HTTPException
from app.cache.redis_client import redis_client

def ip_key(request:Request):
    return f"rate:ip:{request.client.host}"

def user_key(request:Request):
    user = request.state.user
    return f"rate:user:{user.id}"

def rate_limit(limit:int, window:int, key_func):
    def limiter(request:Request):
        key = key_func(request)

        current = redis_client.get(key)

        if current is None:
            redis_client.setex(key, window, 1)
            return

        if int(current) >= limit:
            ttl = redis_client.ttl(key)
            if ttl<0:
                ttl = window
            raise HTTPException(status_code=429, detail=f"Too many requests. Please try again after {ttl} seconds.")

        redis_client.incr(key)
    return limiter