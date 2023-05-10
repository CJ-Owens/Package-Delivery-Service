# C950 Christopher Owens 010682412
import datetime

from package import load_package_data
from address import load_distance_data
from address import load_address_data
from truck import Truck

package_hash = load_package_data('packageCSV.csv')
distance_list = load_distance_data('distanceCSV.csv')
address_list = load_address_data('addressCSV.csv')


# Function to find distance between addresses
# Big-O (1)
def address_dist_between(address1, address2):
    # If distance array has exception due to invalid index at -1, print 'Bad address'
    distance_between = -1
    address1_index = -1
    address2_index = -1
    try:
        address1_index = address_list.index(address1)
        address2_index = address_list.index(address2)
        # address1 index has to be < address2, if it isn't then swap the index of address1 and address2
        if address1_index <= address2_index:
            distance_between = distance_list[address2_index][address1_index]
        else:
            distance_between = distance_list[address1_index][address2_index]
    except IndexError:
        print('Bad address', address1_index, address1, address2_index, address2)
    return distance_between


# Create 3 truck objects with packages sorted
truck_1 = Truck(1, [1, 7, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 37, 39], datetime.timedelta(hours=8))
truck_2 = Truck(2, [2, 3, 5, 9, 12, 18, 22, 24, 27, 33, 35, 36, 38], datetime.timedelta(hours=10, minutes=20))
truck_3 = Truck(3, [4, 6, 10, 11, 17, 23, 25, 26, 28, 31, 32, 40], datetime.timedelta(hours=9, minutes=5))


# Load packages and deliver truck
# Big-O (n^3)
def deliver_truck(truck):
    current_address = address_list[0]
    current_time = truck.starting_time
    truck_mileage = 0
    # Iterate through truck's packages
    # O(n)
    while len(truck.package_list) > 0:
        minimum_distance = 999
        minimum_package = None
        # O(n)
        for p_id in truck.package_list:
            # O(n) hash table search
            truck_package = package_hash.search(p_id)
            truck_package.status = 'En Route'
            distance = address_dist_between(current_address, truck_package.address)
            # Find minimum distance between current address and remaining packages on truck
            if distance < minimum_distance:
                minimum_distance = distance
                minimum_package = truck_package

        if minimum_package is not None:
            # Calculate time traveled
            current_time = current_time + datetime.timedelta(hours=minimum_distance/18)
            current_address = minimum_package.address
            # Mark the packages delivered
            minimum_package.delivery_time = current_time
            minimum_package.status = 'Delivered'
            minimum_package.departure_time = truck.starting_time
            truck_mileage += minimum_distance
            if len(truck.package_list) == 1:
                return_to_hub = address_dist_between(minimum_package.address, address_list[0])
                current_time = current_time + datetime.timedelta(hours=return_to_hub / 18)
                truck_mileage += return_to_hub
                # Remove package from truck after delivered
            truck.package_list.remove(minimum_package.id)
            # Add distance truck traveled for each package for truck_mileage

    return current_time, truck_mileage


# Call function deliver_truck to deliver packages for each truck
truck_1.finish_time, truck1_distance = deliver_truck(truck_1)

# Change package 9 address before loading on truck
package_9 = package_hash.search(9)
package_9.address = '410 S State St'
package_9.city = 'Salt Lake City'
package_9.state = 'UT'
package_9.zip = '84111'

# Make sure there are only two trucks out at a time
if truck_1.conflicts_with(truck_2):
    truck_2.starting_time = truck_1.finish_time

# Deliver remaining trucks
truck_2.finish_time, truck2_distance = deliver_truck(truck_2)
truck_3.finish_time, truck3_distance = deliver_truck(truck_3)


# User Interface
# Worst case big-O (n^3)
user_input = None
while user_input != '4':
    print('*****************************************************')
    print('Total Miles: ', truck1_distance + truck2_distance + truck3_distance)
    print('*****************************************************')
    print('1. Print All Package Statuses')
    print('2. Get Single Package Status with a Time')
    print('3. Get All Package Status with a Time')
    print('4. Exit the Program')
    print('*****************************************************')
    user_input = input('Enter Selection: ')

    # When user inputs '1': Print all package data
    if user_input == '1':
        for package_id in range(1, 41):
            package = package_hash.search(package_id)
            print(package)

    # When user inputs '2': Print status selected package at input time
    elif user_input == '2':
        get_id = int(input('Enter Package ID: '))
        get_time = input("Enter time: ")
        # Split the input string and type as int for use in datetime.timedelta method
        hours, minutes = get_time.split(':')
        user_time = datetime.timedelta(hours=int(hours), minutes=int(minutes))
        try:
            package = package_hash.search(get_id)
            print(package.status_at_time(user_time))
        except AttributeError:
            print('Invalid Package ID')

    # When user inputs '3': Print status of all packages at the input time
    elif user_input == '3':
        get_time = input("Enter time: ")
        # Split the input string and type as int for use in datetime.timedelta method
        hours, minutes = get_time.split(':')
        user_time = datetime.timedelta(hours=int(hours), minutes=int(minutes))
        # Iterate through packages here passing to package class
        for package_id in range(1, 41):
            package = package_hash.search(package_id)
            print(package.status_at_time(user_time))

    # When user inputs '4': Option to exit program
    elif user_input == '4':
        print('Program Ended')
        exit()

    # When user inputs something other than numbers 1, 2, 3, 4 : Prompt invalid input
    else:
        print('Input Invalid\nPlease Try Again')
