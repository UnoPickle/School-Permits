from dataclasses import dataclass

@dataclass
class Student:
    user_id: int
    permits: list
    groups: list

    @staticmethod
    def from_db(value: tuple):
        return Student(value[0], value[1], value[2])