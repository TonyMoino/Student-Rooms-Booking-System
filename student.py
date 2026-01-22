from person import Person

class Student(Person):
    def __init__(self, student_id, name):
        super().__init__(name)
        self.student_id = student_id

    def display(self):
        return f"{self.student_id} - {self.name}"

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name
        }

    @staticmethod
    def from_dict(data):
        return Student(data["student_id"], data["name"])
