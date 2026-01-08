from sqlalchemy.orm import Session
from app.schema.category import CategoryBase, CategoryCreate
from app.db.models.category import Category

def add_categories(db:Session, category:CategoryBase):
    db_category = Category(**category.model_dump())
    if not db_category:
        return False
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db:Session) -> CategoryCreate:
    result = db.query(Category).all()
    if not result:
        return False
    return result

def update_category(db:Session, id:int, new_category:CategoryBase):
    db_category = db.get(Category, id)
    if not db_category:
        return False
    db_category.name = new_category.name
    db.commit()
    db.refresh(db_category)
    return db_category
