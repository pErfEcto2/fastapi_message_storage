import datetime
from ..interface import DB
from ..models import Record, User
import uuid

data: list[Record] = []
users: list[User] = []

def new_db() -> DB:
    return __memoryDB()

class __memoryDB(DB):
    def __init__(self) -> None:
        super().__init__()

    def add_user(self, u: User) -> None:
        if u in users:
            return
        
        users.append(u)

    def user_exists_by_name(self, name: str) -> bool:
        for u in users:
            if u.name == name:
                return True
        return False

    def user_has_data_by_id(self, user: User, data_id: str) -> bool:
        for record in data:
            if record.username != user.name:
                continue

            if record.id == data_id:
                return True

        return False



    def get_user_by_name(self, name: str) -> User | None:
        for u in users:
            if u.name == name:
                return u
        return None

    def get_all_users(self) -> list[User]:
        return users

    def get_record(self, data_id: str) -> Record | None:
        for r in data:
            if r.id == data_id:
                return r

    def delete_record(self, data_id: str) -> None:
        for i, record in enumerate(data):
            if record.id == data_id:
                data.pop(i)
                return

    def delete_user(self, u: User) -> None:
        try:
            users.remove(u)
            for i, record in enumerate(data):
                if record.username == u.name:
                    data.pop(i)
        except ValueError:
            pass

    def user_exists(self, u: User) -> bool:
        return u in users

    def add_data_by_name(self, name: str, d: str) -> bool:
        for u in users:
            if u.name != name:
                continue

            data.append(Record(id=str(uuid.uuid7()), username=u.name, data=d))
            return True

        return False

    def add_data(self, u: User, d: str) -> bool:
        if u not in users:
            return False
        
        data.append(Record(id=str(uuid.uuid7()), username=u.name, data=d))
        return True

    def get_all_records(self) -> list[Record]:
        return data

    def change_data(self, data_id: str, d: str) -> None:
        for i, record in enumerate(data):
            if record.id != data_id:
                continue

            data[i].data = d
            data[i].timestamp = datetime.datetime.now()
