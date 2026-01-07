from fastapi import HTTPException, Depends, APIRouter
from app.services.category_service import add_categories
from app.schema.category import CategoryBase
from sqlalchemy.orm import Session
from app.deps.auth import get_current_user
from app.deps.db import get_db
from app.db.models.user import Users
from app.services.category_service import add_categories, get_categories

router = APIRouter(prefix="/Categories", tags=["Category"])

@router.post("/add_category")
async def add_new_category(category:CategoryBase, db:Session=Depends(get_db), current_user:Users = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=401, detail="Admins only")
    db_category = add_categories(db, category)
    if not db_category:
        raise HTTPException(status_code=400, detail="Invalid input")
    return {"msg" : "Category added successfully"}

@router.get("/see_all_categories")
def see_categories(db:Session=Depends(get_db)):
    result = get_categories(db)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return result