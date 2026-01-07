from sqlalchemy.orm import Session
from app.schema.category import CategoryBase
from app.db.models.category import Category

def add_categories(db:Session, category:CategoryBase):
    db_category = Category(**category.model_dump())
    if not db_category:
        return False
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db:Session):
    result = db.query(Category).all()
    if not result:
        return False
    return result