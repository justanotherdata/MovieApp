import redis

# Create a Redis connection and client
redis_client = redis.Redis(host='localhost', port=6379, db=1)