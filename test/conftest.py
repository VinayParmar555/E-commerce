import fakeredis
from unittest.mock import patch

fake_redis = fakeredis.FakeRedis(decode_responses=False)
patch("app.cache.redis_client.redis_client", fake_redis).start()