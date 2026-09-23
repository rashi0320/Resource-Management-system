import math
from datetime import datetime


class Resource:
    """Resource model representing a shared facility with capacity and pricing."""

    def __init__(
        self,
        resource_id: str,
        name: str,
        capacity: int,
        first_hour_rate: float,
        additional_hour_rate: float,
    ):
        self.resource_id = resource_id
        self.name = name
        self.capacity = capacity
        self.first_hour_rate = first_hour_rate
        self.additional_hour_rate = additional_hour_rate
        self.active_sessions = {}  # {user_id: start_time}

    def is_available(self) -> bool:
        """Check if slots are available."""
        return len(self.active_sessions) < self.capacity

    def start_usage(self, user_id: str, start_time: datetime = None) -> bool:
        """Start using the resource if capacity permits."""
        if not self.is_available():
            print(
                f"[REJECTED] Resource '{self.name}' is full. Cannot allocate slot for user {user_id}."
            )
            return False

        if user_id in self.active_sessions:
            print(f"[ERROR] User {user_id} is already using {self.name}.")
            return False

        if start_time is None:
            start_time = datetime.now()

        self.active_sessions[user_id] = start_time
        print(
            f"[STARTED] User {user_id} started using '{self.name}' at {start_time.strftime('%I:%M %p')}."
        )
        return True

    def stop_usage(self, user_id: str, end_time: datetime = None) -> dict:
        """Stop using the resource, calculate bill, and free up capacity."""
        if user_id not in self.active_sessions:
            print(
                f"[ERROR] No active usage found for user {user_id} in {self.name}."
            )
            return None

        start_time = self.active_sessions.pop(user_id)

        if end_time is None:
            end_time = datetime.now()

        # Calculate duration in minutes and hours
        duration_seconds = (end_time - start_time).total_seconds()
        duration_minutes = duration_seconds / 60.0

        # Billing rule: Any fraction of an hour rounds up to the next complete hour
        billed_hours = math.ceil(duration_minutes / 60.0)
        if billed_hours == 0:
            billed_hours = 1  # Minimum 1 hour charge if started

        # Calculate Total Amount
        if billed_hours == 1:
            total_bill = self.first_hour_rate
        else:
            total_bill = self.first_hour_rate + (
                (billed_hours - 1) * self.additional_hour_rate
            )

        bill_details = {
            "user_id": user_id,
            "resource_name": self.name,
            "start_time": start_time.strftime("%I:%M %p"),
            "end_time": end_time.strftime("%I:%M %p"),
            "duration_minutes": round(duration_minutes, 2),
            "billed_hours": billed_hours,
            "total_bill_inr": total_bill,
        }

        print("\n--- BILL GENERATED ---")
        print(f"User ID        : {bill_details['user_id']}")
        print(f"Resource       : {bill_details['resource_name']}")
        print(f"Start Time     : {bill_details['start_time']}")
        print(f"End Time       : {bill_details['end_time']}")
        print(
            f"Billed Duration: {billed_hours} hour(s) ({round(duration_minutes, 1)} mins)"
        )
        print(f"Total Bill     : ₹{total_bill}")
        print("----------------------\n")

        return bill_details


class BillingSystem:
    """In-memory manager for resources and usage tracking."""

    def __init__(self):
        self.resources = {}

    def add_resource(
        self,
        resource_id: str,
        name: str,
        capacity: int,
        first_hour_rate: float,
        additional_hour_rate: float,
    ):
        resource = Resource(
            resource_id, name, capacity, first_hour_rate, additional_hour_rate
        )
        self.resources[resource_id] = resource
        print(
            f"[SYSTEM] Added Resource: {name} (Capacity: {capacity}, First Hour: ₹{first_hour_rate}, Add. Hour: ₹{additional_hour_rate})"
        )

    def get_resource(self, resource_id: str) -> Resource:
        return self.resources.get(resource_id)


# Demo and Test Cases (Running the Assignment Example)
if __name__ == "__main__":
    system = BillingSystem()

    # 1. Setup Resource: Meeting Room with Capacity = 1, First Hour = 30, Add. Hour = 10
    system.add_resource(
        resource_id="RES01",
        name="Meeting Room A",
        capacity=1,
        first_hour_rate=30.0,
        additional_hour_rate=10.0,
    )

    room = system.get_resource("RES01")

    # 2. Test Case from Assignment: 10:00 AM to 11:20 AM
    start_time = datetime.strptime("10:00 AM", "%I:%M %p")
    end_time = datetime.strptime("11:20 AM", "%I:%M %p")

    print("\n--- TEST CASE 1: Standard Billing Test ---")
    room.start_usage("User_1", start_time=start_time)
    room.stop_usage("User_1", end_time=end_time)

    # 3. Test Case 2: Capacity Full Test
    print("--- TEST CASE 2: Over-capacity Rejection Test ---")
    room.start_usage("User_2", start_time=datetime.now())
    # Resource capacity is 1, so User_3 should be rejected
    room.start_usage("User_3", start_time=datetime.now())

    # Stop User_2 and release capacity
    room.stop_usage("User_2", end_time=datetime.now())

    # User_3 can now start usage
    room.start_usage("User_3", start_time=datetime.now())
    room.stop_usage("User_3", end_time=datetime.now())