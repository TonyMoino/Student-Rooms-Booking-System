import json
from room import Room
from student import Student
from booking import Booking
from admin import Admin

# -------------------------------
# Booking System Controller
# -------------------------------
class BookingSystem:
    def __init__(self):
        self.rooms = []
        self.students = []
        self.bookings = []
        self.admin = Admin()

        self.load_rooms()
        self.load_students()
        self.load_bookings()

    # -------------------------------
    # PROGRAM START
    # -------------------------------
    def start(self):
        while True:
            print("\nWelcome to the Booking System")
            print("1. Student")
            print("2. Admin")
            print("0. Exit")

            choice = input("Select option: ")

            # Student login
            if choice == "1":
                self.student_login()

            # Admin login
            elif choice == "2":
                print("\nAdmin Login")
                if self.admin.login():
                    print(f"\nWelcome, {self.admin.name}!")
                    self.run_admin_menu()
                else:
                    print("Admin login failed.")

            # Exit
            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

    # -------------------------------
    # LOAD METHODS
    # -------------------------------
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

    # -------------------------------
    # SAVE METHODS
    # -------------------------------
    def save_rooms(self):
        with open("rooms.json", "w") as f:
            json.dump([r.to_dict() for r in self.rooms], f, indent=4)

    def save_students(self):
        with open("students.json", "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def save_bookings(self):
        with open("bookings.json", "w") as f:
            json.dump([b.to_dict() for b in self.bookings], f, indent=4)

    # -------------------------------
    # STUDENT LOGIN + MENU
    # -------------------------------
    def student_login(self):
        print("\nStudent Login")
        temp_student = Student("", "", "")

        try:
            with open("students.json", "r") as f:
                students_data = json.load(f)
        except FileNotFoundError:
            print("No students registered.")
            return

        if temp_student.login(students_data):
            print(f"\nWelcome, {temp_student.name}!")
            self.student_menu(temp_student)
        else:
            print("Student login failed.")

    def student_menu(self, student):
        while True:
            print("\nSTUDENT MENU")
            print("1. View Available Rooms")
            print("2. View My Bookings")
            print("0. Logout")

            choice = input("Select option: ")

            # View available rooms
            if choice == "1":
                found = False
                for r in self.rooms:
                    if r.available:
                        print(r.display())
                        found = True
                if not found:
                    print("No available rooms.")

            # View own bookings
            elif choice == "2":
                found = False
                for b in self.bookings:
                    if b.student_id == student.person_id:
                        print(b.display())
                        found = True
                if not found:
                    print("No bookings found.")

            # Logout
            elif choice == "0":
                print("Logged out.")
                break

            else:
                print("Invalid option.")

    # -------------------------------
    # ADMIN MENU
    # -------------------------------
    def run_admin_menu(self):
        while True:
            print("\nADMIN MENU")
            print("1. View Rooms")
            print("2. View Students")
            print("3. View Bookings")
            print("4. Add Room")
            print("5. Delete Room")
            print("6. Add Student")
            print("7. Delete Student")
            print("8. Book Room")
            print("9. Cancel Booking")
            print("A. Add Admin")
            print("D. Delete Admin")
            print("0. Logout")

            choice = input("Select option: ")

            if choice == "1":
                self.view_rooms()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.view_bookings()
            elif choice == "4":
                self.add_room()
            elif choice == "5":
                self.delete_room()
            elif choice == "6":
                self.add_student()
            elif choice == "7":
                self.delete_student()
            elif choice == "8":
                self.book_room()
            elif choice == "9":
                self.cancel_booking()
            elif choice == "A":
                self.admin.add_admin()
            elif choice == "D":
                self.admin.delete_admin()
            elif choice == "0":
                print("Logged out.")
                break
            else:
                print("Invalid option.")

    # -------------------------------
    # ADMIN VIEW METHODS
    # -------------------------------
    def view_rooms(self):
        if not self.rooms:
            print("No rooms available.")
        for r in self.rooms:
            print(r.display())

    def view_students(self):
        if not self.students:
            print("No students registered.")
        for s in self.students:
            print(s.display())

    def view_bookings(self):
        if not self.bookings:
            print("No bookings made.")
        for b in self.bookings:
            print(b.display())

    # -------------------------------
    # ADMIN ACTION METHODS
    # -------------------------------
    def add_student(self):
        sid = input("Student ID: ")
        name = input("Student Name: ")
        password = input("Student Password: ")

        self.students.append(Student(sid, name, password))
        self.save_students()
        print("Student added and saved.")

    def delete_student(self):
        sid = input("Student ID to delete: ")
        self.students = [s for s in self.students if s.person_id != sid]
        self.save_students()
        print("Student deleted and saved.")

    def add_room(self):
        rid = int(input("Room ID: "))
        rtype = input("Room Type: ")
        price = float(input("Price: "))

        self.rooms.append(Room(rid, rtype, price, True))
        self.save_rooms()
        print("Room added and saved.")

    def delete_room(self):
        rid = int(input("Room ID to delete: "))
        self.rooms = [r for r in self.rooms if r.room_id != rid]
        self.save_rooms()
        print("Room deleted and saved.")

    def book_room(self):
        sid = input("Student ID: ")
        rid = int(input("Room ID: "))

        for r in self.rooms:
            if r.room_id == rid and r.available:
                r.available = False
                self.bookings.append(Booking(sid, rid))
                self.save_rooms()
                self.save_bookings()
                print("Room booked and saved.")
                return

        print("Room not available or not found.")

    def cancel_booking(self):
        sid = input("Student ID: ")
        rid = int(input("Room ID: "))

        self.bookings = [
            b for b in self.bookings
            if not (b.student_id == sid and b.room_id == rid)
        ]

        for r in self.rooms:
            if r.room_id == rid:
                r.available = True

        self.save_rooms()
        self.save_bookings()
        print("Booking cancelled and saved.")
