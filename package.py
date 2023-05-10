from hashtable import ChainingHashTable


# Class to create package objects
# Big O (1)
class Package:
    def __init__(self, p_id, address, city, state, p_zip, deadline_time, weight, notes):
        self.id = p_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = p_zip
        self.deadline_time = deadline_time
        self.weight = weight
        self.notes = notes
        self.status = 'At hub'
        self.departure_time = None
        self.delivery_time = None

    # Print function when calling hashtable search for object stored in hash
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city, self.state,
                                                       self.zip, self.deadline_time, self.delivery_time,
                                                       self.weight, self.status)

    # Function status of object at time
    def status_at_time(self, time):

        status = 'At Hub'

        if self.delivery_time < time:
            status = 'Delivered'
        elif self.departure_time < time:
            status = 'En Route'

        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city, self.state,
                                                       self.zip, self.deadline_time, self.delivery_time, self.weight,
                                                       status)


package_hash = ChainingHashTable()


# Load package hash table from package csv file
# Big O (n)
def load_package_data(package_csv):
    import csv
    with open(package_csv, encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=',')

        for row in reader:
            p_id = int(row[0])
            p_address = row[1]
            p_city = row[2]
            p_state = row[3]
            p_zip = row[4]
            p_delivery_time = row[5]
            p_weight = row[6]
            p_notes = row[7]
            # Create package object
            package_object = Package(p_id, p_address, p_city, p_state, p_zip, p_delivery_time, p_weight, p_notes)
            # Insert package into hash table
            package_hash.insert(package_object.id, package_object)
    return package_hash
