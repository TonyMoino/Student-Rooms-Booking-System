# -------------------------------
# Booking Class
# -------------------------------
class Booking:
    def __init__(self, student_id, room_id):
        self.student_id = student_id
        self.room_id = room_id

    def display(self):
        return f"Student {self.student_id} booked Room {self.room_id}"

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "room_id": self.room_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["room_id"])
