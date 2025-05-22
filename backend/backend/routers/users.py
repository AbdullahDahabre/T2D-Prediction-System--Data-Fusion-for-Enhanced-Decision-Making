from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User as DBUser
from schemas import UserOut, UserUpdate
from auth import get_current_user

router = APIRouter()

# Only admin can view/edit/delete all users
def is_admin(current_user: DBUser):
    return current_user.role == "admin"

@router.get("/users", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Only admin can access this.")
    return db.query(DBUser).all()

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if current_user.id != user.id and not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized.")
    return user

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, updated: UserUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if current_user.id != user.id and not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized.")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Only admin can delete users.")
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted."}