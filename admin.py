import json
from person import Person

# -------------------------------
# Admin Class
# -------------------------------
class Admin(Person):
    def __init__(self, admin_id="A001", name="admin1", active=True):
        super().__init__(admin_id, name, "Admin", active)
        self.admins = []
        self.load_admins()

    # Load admins from JSON
    def load_admins(self):
        try:
            with open("admins.json", "r") as f:
                self.admins = json.load(f)
        except FileNotFoundError:
            # Default admin
            self.admins = [
                {
                    "person_id": "A001",
                    "name": "admin1",
                    "role": "Admin",
                    "active": True,
                    "password": "1234"
                }
            ]
            self.save_admins()

    # Save admins to JSON
    def save_admins(self):
        with open("admins.json", "w") as f:
            json.dump(self.admins, f, indent=4)

    # Authenticate admin
    def login(self):
        name = input("Admin name: ")
        pwd = input("Admin password: ")

        for admin in self.admins:
            if (admin["name"] == name and
                admin["password"] == pwd and
                admin.get("active", True)):

                self.person_id = admin["person_id"]
                self.name = admin["name"]
                self.active = admin["active"]
                return True

        return False

    # Add new admin
    def add_admin(self):
        admin_id = input("New Admin ID: ")
        name = input("New Admin Name: ")
        password = input("New Admin Password: ")

        self.admins.append({
            "person_id": admin_id,
            "name": name,
            "role": "Admin",
            "active": True,
            "password": password
        })

        self.save_admins()
        print("Admin added and saved.")

    # Delete admin
    def delete_admin(self):
        if len(self.admins) <= 1:
            print("Cannot delete the last admin.")
            return

        admin_id = input("Admin ID to delete: ")

        for admin in self.admins:
            if admin["person_id"] == admin_id:
                self.admins.remove(admin)
                self.save_admins()
                print("Admin deleted and saved.")
                return

        print("Admin not found.")
