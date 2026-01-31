from person import Person

# -------------------------------
# Student Class
# -------------------------------
class Student(Person):
    def __init__(self, student_id, name, password, active=True):
        super().__init__(student_id, name, "Student", active)
        self.password = password

    # Authenticate student
    def login(self, students_data):
        name = input("Student name: ")
        pwd = input("Student password: ")

        for student in students_data:
            if (student["name"] == name and
                student["password"] == pwd and
                student.get("active", True)):

                self.person_id = student["person_id"]
                self.name = student["name"]
                self.active = student["active"]
                return True

        return False

    # Convert to dictionary
    def to_dict(self):
        data = super().to_dict()
        data["password"] = self.password
        return data

    # Create Student from dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["person_id"],
            data["name"],
            data["password"],
            data.get("active", True)
        )
