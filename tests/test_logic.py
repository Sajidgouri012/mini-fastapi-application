from crud import count_items_custom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models, os

# Unit test for business logic: count_items_custom uses raw SQL; test it on an empty DB then after insert.
def test_count_items_custom(tmp_path, monkeypatch):
    db_path = tmp_path / "tmp.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    models.Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    # empty DB
    res = count_items_custom(s)
    assert res["total"] == 0
    # insert an item
    it = models.Item(title="hello", description="desc")
    s.add(it)
    s.commit()
    res2 = count_items_custom(s)
    assert res2["total"] == 1
    s.close()
