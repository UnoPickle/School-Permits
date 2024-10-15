from dataclasses import dataclass
@dataclass
class Student:
    first_name: str
    last_name: str
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

@dataclass
class Teacher:
    first_name: str
    last_name: str
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'