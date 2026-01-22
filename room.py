class Room:
    def __init__(self, room_id, room_type, price, available=True):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.available = available

    def book(self):
        if self.available:
            self.available = False
            return True
        return False

    def cancel(self):
        self.available = True

    def display(self):
        status = "Available" if self.available else "Booked"
        return f"Room {self.room_id} | {self.room_type} | ${self.price} | {status}"

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_type": self.room_type,
            "price": self.price,
            "available": self.available
        }

    @staticmethod
    def from_dict(data):
        return Room(
            data["room_id"],
            data["room_type"],
            data["price"],
            data["available"]
        )
