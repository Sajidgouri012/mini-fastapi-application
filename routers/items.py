from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/", response_model=schemas.ItemOut, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(item: schemas.ItemCreate, db: Session = Depends(get_db), related_update_id: Optional[int] = None):
    """
    Create an item. If `related_update_id` is provided, update that item inside the same transaction.
    Demonstrates transaction handling.
    """
    try:
        # begin transaction
        with db.begin():
            new_item = crud.create_item(db, item)
            # optional related update in same transaction
            if related_update_id:
                other = crud.get_item(db, related_update_id)
                if not other:
                    raise HTTPException(status_code=404, detail="Related item to update not found")
                other.description = (other.description or "") + "\nUpdated by transaction"
                db.add(other)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error (maybe duplicate title)")
    return new_item

@router.get("/", response_model=List[schemas.ItemOut])
def list_items(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0), title: Optional[str] = Query(None), db: Session = Depends(get_db)):
    items = crud.get_items(db, limit=limit, offset=offset, title_filter=title)
    return items

@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=schemas.ItemOut)
def update_item(item_id: int, updates: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        updated = crud.update_item(db, db_item, updates)
        db.commit()
        db.refresh(updated) 
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error (maybe duplicate title)")
    return updated

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, db_item)
    db.commit()
    return JSONResponse(content = {"msg":"item deleted successfully"}, status_code=200)

@router.get("/summary/", response_model=dict)
def summary(contains: Optional[str] = None, db: Session = Depends(get_db)):
    # custom SQL via ORM layer
    res = crud.count_items_custom(db, contains=contains)
    return res
