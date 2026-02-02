class Admin:

    PASSWORD= "1234"

    @staticmethod
    def login():
        print("\n🔐 Admin Login")
        password = input("Password: ")

        if  password == Admin.PASSWORD:
            print("✅ Login successful")
            return True

        print("❌ Invalid credentials")
        return False
