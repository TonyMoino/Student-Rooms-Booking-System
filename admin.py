class Admin:
    def __init__(self):
        self.admins = {
            "admin1": "1234",
            "admin2": "1234",
            "admin3": "1234"
        }

    def login(self):
        user = input("Admin username: ")
        pwd = input("Admin password: ")
        return user in self.admins and self.admins[user] == pwd

    def add_admin(self):
        user = input("New admin username: ")
        pwd = input("New admin password: ")
        self.admins[user] = pwd
        print("Admin added.")
