# -------------------------------
# Advanced Person Base Class
# -------------------------------
class Person:
    def __init__(self, person_id, name, role, active=True):
        self.person_id = person_id
        self.name = name
        self.role = role
        self.active = active

    # Display basic person info
    def display(self):
        status = "Active" if self.active else "Inactive"
        return f"{self.role} | {self.person_id} | {self.name} | {status}"

    # Convert base data to dictionary
    def to_dict(self):
        return {
            "person_id": self.person_id,
            "name": self.name,
            "role": self.role,
            "active": self.active
        }
