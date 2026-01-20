from pytest import fixture, raises
from app.storage.interface import DB
from app.storage.models import User
from app.storage.memory.storage import new_db



@fixture
def db_instance():
    db = new_db()
    yield db
    db.clear()

def test_add_user(db_instance: DB):
    u = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u)
    assert db_instance.get_all_users() == [u]

    u_copy = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u_copy)
    assert db_instance.get_all_users() == [u]

def test_get_all_users(db_instance: DB):
    assert db_instance.get_all_users() == []

    u1 = User(name="test 1", hashed_pwd="test", salt="test")
    u2 = User(name="test 2", hashed_pwd="test", salt="test")

    db_instance.add_user(u1)
    db_instance.add_user(u2)

    users = db_instance.get_all_users()
    assert all([u in users for u in [u1, u2]])


def test_get_user_by_name(db_instance: DB):
    u = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u)

    assert db_instance.get_user_by_name(u.name) == u
    assert db_instance.get_user_by_name("does not exist") is None


def test_user_exists_by_name(db_instance: DB):
    u = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u)

    assert db_instance.user_exists_by_name(u.name)
    assert not db_instance.user_exists_by_name("does not exist")

def test_delete_user(db_instance: DB):
    u = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u)
    db_instance.add_data(u, "test data")

    db_instance.delete_user(u)
    assert db_instance.get_all_users() == []
    assert db_instance.get_all_records() == []

def test_user_exists(db_instance: DB):
    u = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u)
    assert db_instance.user_exists(u)

def test_add_data_by_name(db_instance: DB):
    u = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u)
    db_instance.add_data_by_name(u.name, "test data")
    r = db_instance.get_all_records()[0]
    assert r.username == u.name
    assert r.data == "test data"

    u = User(name="test 2", hashed_pwd="test", salt="test")
    assert not db_instance.add_data_by_name(u.name, "test data 2")

def test_add_data(db_instance: DB):
    u = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u)
    assert db_instance.add_data(u, "test data")
    r = db_instance.get_all_records()[0]
    assert r.username == u.name
    assert r.data == "test data"

    u = User(name="test 2", hashed_pwd="test", salt="test")
    assert not db_instance.add_data(u, "test data 2")

def test_get_all_records(db_instance: DB):
    u = User(name="test", hashed_pwd="test", salt="test")
    db_instance.add_user(u)
    assert db_instance.add_data(u, "test data 1")
    assert db_instance.add_data(u, "test data 2")

    records = db_instance.get_all_records()
    assert len(records) == 2
    records_data = [record.data for record in records]
    assert all([d in records_data for d in ["test data 1", "test data 2"]])

def test_get_record(db_instance: DB):
    assert db_instance.get_all_records() == []
    u = User(name="test", hashed_pwd="test", salt="test")

    db_instance.add_user(u)
    assert db_instance.add_data(u, "test data")

    records = db_instance.get_all_records()
    assert len(records) == 1
    assert records[0].username == u.name
    assert records[0].data == "test data"

    data_id = records[0].id

    r = db_instance.get_record(data_id)
    assert r is not None
    assert r.username == u.name
    assert r.data == "test data"


def test_delete_record(db_instance: DB):
    assert db_instance.get_all_records() == []
    u = User(name="test", hashed_pwd="test", salt="test")

    db_instance.add_user(u)
    assert db_instance.add_data(u, "test data")

    data_id = db_instance.get_all_records()[0].id
    db_instance.delete_record(data_id)

    assert db_instance.get_all_records() == []

def test_change_data(db_instance: DB):
    assert db_instance.get_all_records() == []
    u = User(name="test", hashed_pwd="test", salt="test")

    db_instance.add_user(u)
    assert db_instance.add_data(u, "test data")
    assert db_instance.add_data(u, "test data 2")
    
    r = db_instance.get_all_records()[0]
    data_id = r.id

    db_instance.change_data(data_id, "new test data")
    r_copy = db_instance.get_all_records()[0]

    assert r.id == r_copy.id
    assert r.username == r_copy.username
    assert r.timestamp == r_copy.timestamp
    assert r_copy.data == "new test data"

def test_user_has_data_by_id(db_instance: DB):
    assert db_instance.get_all_records() == []
    u1 = User(name="test1", hashed_pwd="test", salt="test")
    u2 = User(name="test2", hashed_pwd="test", salt="test")

    db_instance.add_user(u1)
    db_instance.add_user(u2)
    assert db_instance.add_data(u1, "test data")
    
    r = db_instance.get_all_records()[0]
    data_id = r.id

    assert db_instance.user_has_data_by_id(u1, data_id)
    assert not db_instance.user_has_data_by_id(u1, "does not exist")
    assert not db_instance.user_has_data_by_id(u2, "does not exist")
