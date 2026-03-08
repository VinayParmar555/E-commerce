from sqlalchemy.orm import Session
from app.cache.redis_client import redis_client
from app.services.product_service import List_of_products
import msgpack

def get_cached_products(db:Session):
    cache_key = "products:list"
    cached = redis_client.get(cache_key)
    if cached:
        return msgpack.unpackb(cached, raw=False)
    products = List_of_products(db)
    
    if not products:
        return []

    result = [
        {
            "id" : p.id, 
            "name" : p.name,
            "price" : p.price,
            "description" : p.description,
            "quantity" : p.quantity,
            "category" : p.category.name if p.category else None
            
        }
        for p in products
    ]
    redis_client.setex(cache_key, 60 * 5, msgpack.packb(result))
    return result

def delete_cached_product(product_id:int):
    redis_client.delete("products:list")
    redis_client.delete(f"product:{product_id}")