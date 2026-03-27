from datetime import datetime
from fastapi.encoders import jsonable_encoder

fake_db :dict[int, dict] = {}
_id_counter = 0

def next_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter


def get_all() -> list[dict]:
    return list(fake_db.values())


def get_by_id(record_id: int) -> dict | None:
    return fake_db.get(record_id)


def create(data: dict) -> dict:
    record_id = next_id()
    now = datetime.utcnow()
    record = {
        **data,
        "id":         record_id,
        "created_at": now,
        "updated_at": now,
    }
    fake_db[record_id] = jsonable_encoder(record)
    return fake_db[record_id]


def update(record_id: int, data: dict) -> dict:
    existing = fake_db[record_id]
    updated = {
        **existing,
        **data,
        "updated_at": jsonable_encoder(datetime.utcnow())
    }
    fake_db[record_id] = updated
    return fake_db[record_id]


def delete(record_id: int) -> None:
    del fake_db[record_id]