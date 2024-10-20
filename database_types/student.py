
class Student:
    user_id: int
    parent_id: int

    def __init__(self, user_id: int, parent_id: int):
        self.user_id = user_id
        self.parent_id = parent_id



    @staticmethod
    def from_db(value: tuple):
        return Student(value[0], value[1])