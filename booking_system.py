import json
from room import Room
from student import Student
from booking import Booking
from admin import Admin

# Main system controller
class BookingSystem:
    def __init__(self):
        self.rooms = []
        self.students = []
        self.bookings = []
        self.admin = Admin()

        self.load_rooms()
        self.load_students()
        self.load_bookings()

    def load_rooms(self):
        try:
            with open("rooms.json", "r") as f:
                self.rooms = [Room.from_dict(r) for r in json.load(f)]
        except FileNotFoundError:
            self.rooms = []

    def load_students(self):
        try:
            with open("students.json", "r") as f:
                self.students = [Student.from_dict(s) for s in json.load(f)]
        except FileNotFoundError:
            self.students = []

    def load_bookings(self):
        try:
            with open("bookings.json", "r") as f:
                self.bookings = [Booking.from_dict(b) for b in json.load(f)]
        except FileNotFoundError:
            self.bookings = []

    def save_rooms(self):
        with open("rooms.json", "w") as f:
            json.dump([r.to_dict() for r in self.rooms], f, indent=4)

    def save_students(self):
        with open("students.json", "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def save_bookings(self):
        with open("bookings.json", "w") as f:
            json.dump([b.to_dict() for b in self.bookings], f, indent=4)

    def view_rooms(self):
        for r in self.rooms:
            print(r.display())

    def view_students(self):
        for s in self.students:
            print(s.display())

    def view_bookings(self):
        for b in self.bookings:
            print(b.display())

    def add_student(self):
        sid = int(input("Student ID: "))
        if any(s.student_id == sid for s in self.students):
            print("Student exists.")
            return
        name = input("Name: ")
        self.students.append(Student(sid, name))
        self.save_students()
        print("Student added.")

    def delete_student(self):
        sid = int(input("Student ID to delete: "))
        self.students = [s for s in self.students if s.student_id != sid]
        self.save_students()
        print("Student deleted.")

    def add_room(self):
        rid = int(input("Room ID: "))
        if any(r.room_id == rid for r in self.rooms):
            print("Room exists.")
            return
        rtype = input("Room type: ")
        price = float(input("Price: "))
        self.rooms.append(Room(rid, rtype, price))
        self.save_rooms()
        print("Room added.")

    def delete_room(self):
        rid = int(input("Room ID to delete: "))
        self.rooms = [r for r in self.rooms if r.room_id != rid]
        self.save_rooms()
        print("Room deleted.")

    def book_room(self):
        sid = int(input("Student ID: "))
        rid = int(input("Room ID: "))

        student = next((s for s in self.students if s.student_id == sid), None)
        room = next((r for r in self.rooms if r.room_id == rid), None)

        if not student or not room:
            print("Student or room not found.")
            return
        if not room.available:
            print("Room booked.")
            return

        self.bookings.append(Booking(sid, rid))
        room.available = False
        self.save_bookings()
        self.save_rooms()
        print("Booked.")

    def cancel_booking(self):
        sid = int(input("Student ID: "))
        rid = int(input("Room ID: "))

        self.bookings = [b for b in self.bookings if not (b.student_id == sid and b.room_id == rid)]
        room = next((r for r in self.rooms if r.room_id == rid), None)

        if room:
            room.available = True

        self.save_bookings()
        self.save_rooms()
        print("Canceled.")

    def run(self):
        while True:
            print("\n--- MENU ---")
            print("1. View Rooms")
            print("2. View Students")
            print("3. View Bookings")
            print("4. Add Room (Admin)")
            print("5. Delete Room (Admin)")
            print("6. Add Student")
            print("7. Delete Student")
            print("8. Book Room")
            print("9. Cancel Booking")
            print("A. Add Admin (Admin)")
            print("0. Exit")

            choice = input("Choice: ").upper()

            if choice == "1":
                self.view_rooms()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.view_bookings()
            elif choice == "4" and self.admin.login():
                self.add_room()
            elif choice == "5" and self.admin.login():
                self.delete_room()
            elif choice == "6":
                self.add_student()
            elif choice == "7":
                self.delete_student()
            elif choice == "8":
                self.book_room()
            elif choice == "9":
                self.cancel_booking()
            elif choice == "A" and self.admin.login():
                self.admin.add_admin()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")