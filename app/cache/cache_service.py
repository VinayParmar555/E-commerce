from sqlalchemy.orm import Session
from app.cache.redis_client import redis_client
from app.services.product_service import List_of_products
import json

def get_cached_products(db:Session):
    cache_key = "products:list"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    products = List_of_products(db)

    result = [
        {
            "id" : p.id, 
            "name" : p.name,
            "price" : p.price,
            "description" : p.description,
            "quantity" : p.quantity
            
        }
        for p in products
    ]
    redis_client.set(cache_key, json.dumps(result), ex=60 * 5)
    return result
