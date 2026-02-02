class Booking:
    def __init__(self, student, room):
        self.student = student
        self.room = room

    def details(self):
        return f"{self.student.name} booked Room {self.room.room_id}"

    def to_dict(self):
        return {
            "student_id": self.student.student_id,
            "room_id": self.room.room_id
        }
