from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    email: str
    password: str
    name: str
    type: int

    @staticmethod
    def from_db(value: tuple):
        return User(value[0], value[1], value[2], value[3], value[4])

    def get_name(self):
        return self.name