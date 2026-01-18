import abc 
from .models import User, Record


class DB(abc.ABC):
    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def add_user(self, u: User) -> None:
        """
        add an user to the db
        """
        pass

    @abc.abstractmethod
    def delete_user(self, u: User) -> None:
        """
        delete an user from the db
        """
        pass

    @abc.abstractmethod
    def delete_record(self, data_id: str) -> None:
        """
        delete a record with given id
        """
        pass

    @abc.abstractmethod
    def get_record(self, data_id: str) -> Record | None:
        """
        return a record with the given id
        """
        pass

    @abc.abstractmethod
    def get_user_by_name(self, name: str) -> User | None:
        """
        returns user by his name
        if there's no an user with such name returns None instead
        """
        pass

    @abc.abstractmethod
    def user_exists_by_name(self, name: str) -> bool:
        """
        returns true if there's an user with the given name
        false otherwise
        """
        pass

    @abc.abstractmethod
    def user_has_data_by_id(self, user: User, data_id: str) -> bool:
        """
        returns True if the given user has a data with given id
        false otherwise
        """
        pass

    @abc.abstractmethod
    def user_exists(self, u: User) -> bool:
        """
        returns true if the user "u" exists in the db
        false otherwise
        """
        pass

    @abc.abstractmethod
    def add_data(self, u: User, d: str) -> bool:
        """
        adds a data to the given user
        """
        pass

    @abc.abstractmethod
    def change_data(self, data_id: str, d: str) -> None:
        """
        change data of given record
        """
        pass

    @abc.abstractmethod
    def get_all_users(self) -> list[User]:
        """
        returns a list of all users
        """
        pass

    @abc.abstractmethod
    def add_data_by_name(self, name: str, d: str) -> bool:
        """
        adds a data to the given user (by name)
        """
        pass

    @abc.abstractmethod
    def get_all_records(self) -> list[Record]:
        """
        returns a list of all records
        """
        pass
        

