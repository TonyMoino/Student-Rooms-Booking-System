import json
from room import Room
from student import Student
from booking import Booking
from admin import Admin


class BookingSystem:
    def __init__(self):
        # List of all room objects
        self.rooms = []

        # List of all student objects
        self.students = []

        # List of all booking objects
        self.bookings = []

        # Admin controller (handles admin login and admin management)
        self.admin = Admin()

        # Load saved data when system starts
        self.load_rooms()
        self.load_students()
        self.load_bookings()


    # choose whether they are a Student or an Admin
    def start(self):
        while True:
            print("\nWelcome to the Booking System")
            print("1. Student")
            print("2. Admin")
            print("0. Exit")

            # Get user's role choice
            choice = input("Select option: ")

            # ---------------- STUDENT LOGIN ----------------
            if choice == "1":
                self.student_login()

            # ---------------- ADMIN LOGIN ----------------
            elif choice == "2":
                print("\nAdmin Login")

                # Attempt admin login
                if self.admin.login():
                    print(f"\nWelcome, {self.admin.name}!")
                    self.run_admin_menu()
                else:
                    print("Admin login failed.")

            # ---------------- EXIT SYSTEM ----------------
            elif choice == "0":
                print("Goodbye!")
                break

            # ---------------- INVALID OPTION ----------------
            else:
                print("Invalid option.")


    # These methods load system data from JSON files
    # and convert them into Python objects

    def load_rooms(self):
        try:
            with open("rooms.json", "r") as f:
                self.rooms = [Room.from_dict(r) for r in json.load(f)]
        except FileNotFoundError:
            # If file doesn't exist, start with empty list
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

    # These methods save system data back to JSON files
    # so data is not lost when the program closes

    def save_rooms(self):
        with open("rooms.json", "w") as f:
            json.dump([r.to_dict() for r in self.rooms], f, indent=4)

    def save_students(self):
        with open("students.json", "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def save_bookings(self):
        with open("bookings.json", "w") as f:
            json.dump([b.to_dict() for b in self.bookings], f, indent=4)

    # STUDENT LOGIN AND MENU


    # Handles student authentication
    def student_login(self):
        print("\nStudent Login")

        # Temporary student object used only for authentication
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

            if choice == "1":
                found = False

                for r in self.rooms:
                    if r.available:
                        print(r.display())
                        found = True

                if not found:
                    print("No available rooms.")

            elif choice == "2":
                found = False

                # Show only bookings for this student
                for b in self.bookings:
                    if b.student_id == student.person_id:
                        print(b.display())
                        found = True

                if not found:
                    print("No bookings found.")

            elif choice == "0":
                print("Logged out.")
                break

            else:
                print("Invalid option.")


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

            # Get admin's choice
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


    # Display all rooms
    def view_rooms(self):
        if not self.rooms:
            print("No rooms available.")

        for r in self.rooms:
            print(r.display())

    # Display all students
    def view_students(self):
        if not self.students:
            print("No students registered.")

        for s in self.students:
            print(s.display())

    # Display all bookings
    def view_bookings(self):
        if not self.bookings:
            print("No bookings made.")

        for b in self.bookings:
            print(b.display())


    def add_student(self):
        sid = input("Student ID: ")
        name = input("Student Name: ")
        password = input("Student Password: ")

        # Create and store new student object
        self.students.append(Student(sid, name, password))

        self.save_students()
        print("Student added and saved.")

    # Delete a student from the system
    def delete_student(self):
        sid = input("Student ID to delete: ")

        self.students = [s for s in self.students if s.person_id != sid]

        # Save changes
        self.save_students()
        print("Student deleted and saved.")

    # Add a new room
    def add_room(self):
        rid = int(input("Room ID: "))
        rtype = input("Room Type: ")
        price = float(input("Price: "))

        # Create and store new room
        self.rooms.append(Room(rid, rtype, price, True))
        self.save_rooms()
        print("Room added and saved.")

    # Delete a room
    def delete_room(self):
        rid = int(input("Room ID to delete: "))
        self.rooms = [r for r in self.rooms if r.room_id != rid]

        # Save changes
        self.save_rooms()
        print("Room deleted and saved.")

    # Book a room for a student
    def book_room(self):
        sid = input("Student ID: ")
        rid = int(input("Room ID: "))

        # Find the room and check availability
        for r in self.rooms:
            if r.room_id == rid and r.available:
                # Mark room as booked
                r.available = False

                # Create new booking
                self.bookings.append(Booking(sid, rid))

                # Save changes
                self.save_rooms()
                self.save_bookings()
                print("Room booked and saved.")
                return

        # If no available room was found
        print("Room not available or not found.")

    # Cancel a booking
    def cancel_booking(self):
        sid = input("Student ID: ")
        rid = int(input("Room ID: "))

        # Remove booking for this student and room
        self.bookings = [
            b for b in self.bookings
            if not (b.student_id == sid and b.room_id == rid)
        ]

        # Mark room as available again
        for r in self.rooms:
            if r.room_id == rid:
                r.available = True

        # Save changes
        self.save_rooms()
        self.save_bookings()
        print("Booking cancelled and saved.")
