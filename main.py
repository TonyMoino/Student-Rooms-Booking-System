from booking_system import BookingSystem
from admin import Admin

if __name__ == "__main__":
    admin = Admin()
    while not admin.login():
        print("Access denied.\n")
    BookingSystem().run()
