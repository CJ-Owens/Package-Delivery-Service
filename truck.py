# Big O (1)
class Truck:
    def __init__(self, truck_id, package_list, starting_time):
        self.truck_id = truck_id
        self.package_list = package_list
        self.starting_time = starting_time
        self.finish_time = None

    def conflicts_with(self, other_truck):
        # No conflict exists if other_truck leaves after Truck is finished
        if self.finish_time <= other_truck.starting_time:
            return False

        else:
            return True
