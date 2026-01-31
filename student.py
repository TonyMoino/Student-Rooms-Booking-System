from person import Person

# Represents a student
class Student(Person):
    def __init__(self, student_id, name):
        super().__init__(name)
        self.student_id = student_id

    def display(self):
        return f"Student {self.student_id} | {self.name}"

    def to_dict(self):
        return {"student_id": self.student_id, "name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"])
