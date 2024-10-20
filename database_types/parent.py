from dataclasses import dataclass

@dataclass
class Parent:
    user_id: int
    children_ids: list

    @staticmethod
    def from_db(value: tuple):
        return Parent(value[0], value[1])