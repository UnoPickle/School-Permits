from dataclasses import dataclass
@dataclass
class User:
    first_name: str
    last_name: str
    type: int

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'