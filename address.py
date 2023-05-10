import csv


# Load distance data from distanceCSV.csv
# Big O (n^2)
def load_distance_data(distance_csv):
    distance_list = []
    with open(distance_csv, encoding='utf-8-sig') as distance_file:
        dist_reader = csv.reader(distance_file, delimiter=',')
        # For loop iterates of each row and sets the distance_row as each row in distance_list
        for row in dist_reader:
            distance_row = []

            for dist_value in row:
                # Converts non-empty strings to float
                if dist_value != '':
                    distance_row.append(float(dist_value))
                # Empty strings set to 0
                else:
                    distance_row.append(0)
            # Append updated row to distance_list
            distance_list.append(distance_row)
    return distance_list


# Load address data from addressCSV.csv
# Big O (n)
def load_address_data(address_file):
    address_list = []
    with open(address_file, encoding='utf-8-sig') as address_file:
        add_reader = csv.reader(address_file, delimiter=',')
        # Append only addresses into address_list
        for row in add_reader:
            address_list.append(row[2])
    return address_list
