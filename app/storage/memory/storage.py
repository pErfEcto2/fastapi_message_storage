import datetime
from ..interface import DB
from ..models import Record, User
import uuid


def new_db() -> DB:
    return __memoryDB()

class __memoryDB(DB):
    instance = None

    def __new__(cls) -> __memoryDB:
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.users = []
            cls.instance.records = []
        return cls.instance

    # def __init__(self) -> None:
    #     self.records: list[Record] = []
    #     self.users: list[User] = []

    def add_user(self, u: User) -> None:
        if u in self.users:
            return
        
        self.users.append(u)

    def user_exists_by_name(self, name: str) -> bool:
        for u in self.users:
            if u.name == name:
                return True
        return False

    def user_has_data_by_id(self, user: User, data_id: str) -> bool:
        for record in self.records:
            if record.username != user.name:
                continue

            if record.id == data_id:
                return True

        return False

    def get_user_by_name(self, name: str) -> User | None:
        for u in self.users:
            if u.name == name:
                return u
        return None

    def get_all_users(self) -> list[User]:
        return self.users

    def get_record(self, data_id: str) -> Record | None:
        for r in self.records:
            if r.id == data_id:
                return r

    def delete_record(self, data_id: str) -> None:
        for i, record in enumerate(self.records):
            if record.id == data_id:
                self.records.pop(i)
                return

    def delete_user(self, u: User) -> None:
        try:
            self.users.remove(u)
            n = len(self.records)

            for i, record in enumerate(reversed(self.records)):
                if record.username == u.name:
                    self.records.pop(n - i - 1)

        except ValueError:
            pass

    def clear(self) -> None:
        self.records = []
        self.users = []

    def user_exists(self, u: User) -> bool:
        return u in self.users

    def add_data_by_name(self, name: str, d: str) -> bool:
        for u in self.users:
            if u.name != name:
                continue

            self.records.append(Record(id=str(uuid.uuid7()), username=u.name, data=d))
            return True

        return False

    def add_data(self, u: User, d: str) -> bool:
        if u not in self.users:
            return False
        
        self.records.append(Record(id=str(uuid.uuid7()), username=u.name, data=d))
        return True

    def get_all_records(self) -> list[Record]:
        return self.records

    def change_data(self, data_id: str, d: str) -> None:
        for i, record in enumerate(self.records):
            if record.id != data_id:
                continue

            self.records[i].data = d
            self.records[i].timestamp = datetime.datetime.now()
