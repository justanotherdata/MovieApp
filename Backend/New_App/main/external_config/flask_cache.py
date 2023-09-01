from flask_caching import Cache

def make_cache(app):
    cache = Cache(app)
    return cache