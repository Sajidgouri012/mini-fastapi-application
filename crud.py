from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate, ItemUpdate
from sqlalchemy import text


def get_item(db: Session, item_id: int):
    """
    Retrieve a single Item from the database by its ID.
    Returns the Item object if found, otherwise None.
    """
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, limit: int = 10, offset: int = 0, title_filter: str = None):
    """
    Retrieve a list of Items with optional pagination and title filtering.

    Args:
        limit (int): Max number of items to return.
        offset (int): Number of items to skip before starting to return results.
        title_filter (str): Optional filter to match items whose title contains this string.

    Returns:
        List[Item]: A list of Item objects.
    """
    q = db.query(Item)
    if title_filter:
        q = q.filter(Item.title.contains(title_filter))  # Apply filter if provided
    return q.offset(offset).limit(limit).all()


def create_item(db: Session, item: ItemCreate):
    """
    Create a new Item in the database.

    Args:
        item (ItemCreate): Pydantic schema containing 'title' and 'description'.

    Returns:
        Item: The newly created Item object (not yet refreshed).
    """
    db_item = Item(title=item.title, description=item.description)
    db.add(db_item)
    db.flush()  # Assigns an ID from the database without committing
    return db_item


def update_item(db: Session, db_item: Item, updates: ItemUpdate):
    """
    Update an existing Item with new values (if provided).

    Args:
        db_item (Item): The existing Item object to update.
        updates (ItemUpdate): Pydantic schema with optional title/description.

    Returns:
        Item: The updated Item object.
    """
    if updates.title is not None:
        db_item.title = updates.title
    if updates.description is not None:
        db_item.description = updates.description
    db.add(db_item)  # Mark object as "dirty" so SQLAlchemy knows to update it
    return db_item


def delete_item(db: Session, db_item: Item):
    """
    Delete an Item from the database.

    Args:
        db_item (Item): The Item object to delete.
    """
    db.delete(db_item)


def count_items_custom(db: Session, contains: str = None):
    """
    Count items using a custom raw SQL query.

    Args:
        contains (str, optional): If provided, counts only items whose title matches pattern.

    Returns:
        dict: A dictionary containing the total count, e.g. {"total": 5}
    """
    if contains:
        # Parameterized query to prevent SQL injection
        sql = text("""SELECT COUNT(*) as total FROM items WHERE title LIKE :pat""")
        res = db.execute(sql, {"pat": f"%{contains}%"}).fetchone()
    else:
        sql = text("""SELECT COUNT(*) as total FROM items""")
        res = db.execute(sql).fetchone()
    return {"total": res[0] if res else 0}
