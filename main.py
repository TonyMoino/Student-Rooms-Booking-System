import json
from room import Room
from student import Student
from booking import Booking
from admin import Admin


class BookingSystem:
    def __init__(self):
        self.rooms = []
        self.students = []
        self.bookings = []

        self.load_rooms()
        self.load_students()
        self.load_bookings()

    # ---------- LOAD / SAVE ----------
    def load_rooms(self):
        try:
            with open("rooms.json", "r") as f:
                self.rooms = [Room.from_dict(r) for r in json.load(f)]
        except FileNotFoundError:
            self.rooms = []

    def save_rooms(self):
        with open("rooms.json", "w") as f:
            json.dump([r.to_dict() for r in self.rooms], f, indent=4)

    def load_students(self):
        try:
            with open("students.json", "r") as f:
                self.students = [Student.from_dict(s) for s in json.load(f)]
        except FileNotFoundError:
            self.students = []

    def save_students(self):
        with open("students.json", "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def load_bookings(self):
        try:
            with open("bookings.json", "r") as f:
                for b in json.load(f):
                    student = next(s for s in self.students if s.student_id == b["student_id"])
                    room = next(r for r in self.rooms if r.room_id == b["room_id"])
                    room.available = False
                    self.bookings.append(Booking(student, room))
        except FileNotFoundError:
            self.bookings = []

    def save_bookings(self):
        with open("bookings.json", "w") as f:
            json.dump([b.to_dict() for b in self.bookings], f, indent=4)

    # ---------- VIEW ----------
    def view_rooms(self):
        for room in self.rooms:
            print(room.display())

    def view_students(self):
        for student in self.students:
            print(student.display())

    def view_bookings(self):
        for booking in self.bookings:
            print(booking.details())

    # ---------- ROOM ----------
    def add_room(self):
        room_id = int(input("Room ID: "))
        room_type = input("Room Type: ")
        price = float(input("Price: "))
        self.rooms.append(Room(room_id, room_type, price))
        self.save_rooms()

    def delete_room(self):
        room_id = int(input("Room ID to delete: "))
        room = next((r for r in self.rooms if r.room_id == room_id), None)

        if not room:
            print("❌ Room not found")
            return
        if not room.available:
            print("🔒 Cannot delete booked room")
            return

        self.rooms.remove(room)
        self.save_rooms()

    # ---------- STUDENT ----------
    def add_student(self):
        student_id = int(input("Student ID: "))
        name = input("Name: ")
        self.students.append(Student(student_id, name))
        self.save_students()

    def delete_student(self):
        student_id = int(input("Student ID to delete: "))
        for booking in self.bookings:
            if booking.student.student_id == student_id:
                print("🔒 Student has active booking")
                return

        self.students = [s for s in self.students if s.student_id != student_id]
        self.save_students()

    # ---------- BOOKING ----------
    def book_room(self):
        student_id = int(input("Student ID: "))
        room_id = int(input("Room ID: "))

        student = next((s for s in self.students if s.student_id == student_id), None)
        room = next((r for r in self.rooms if r.room_id == room_id), None)

        if not student or not room or not room.book():
            print("❌ Booking failed")
            return

        self.bookings.append(Booking(student, room))
        self.save_rooms()
        self.save_bookings()

    def cancel_booking(self):
        student_id = int(input("Student ID: "))
        for booking in self.bookings:
            if booking.student.student_id == student_id:
                booking.room.cancel()
                self.bookings.remove(booking)
                self.save_rooms()
                self.save_bookings()
                return
        print("❌ Booking not found")


def main():
    if not Admin.login():
        return

    system = BookingSystem()

    while True:
        print("""
1. View Rooms
2. View Students
3. Add Room
4. Delete Room
5. Add Student
6. Delete Student
7. Book Room
8. Cancel Booking
9. View Bookings
0. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            system.view_rooms()
        elif choice == "2":
            system.view_students()
        elif choice == "3":
            system.add_room()
        elif choice == "4":
            system.delete_room()
        elif choice == "5":
            system.add_student()
        elif choice == "6":
            system.delete_student()
        elif choice == "7":
            system.book_room()
        elif choice == "8":
            system.cancel_booking()
        elif choice == "9":
            system.view_bookings()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
