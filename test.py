import csv

# Define your lists
list1 = [1, 2, 3, 4, 5]
list2 = ['a', 'b', 'c', 'd', 'e']
list3 = [True, False, True, False, True]

# Create a list of tuples containing the name and values of each list
lists = [('List 1', list1), ('List 2', list2), ('List 3', list3)]

# Specify the output CSV file path
output_file = 'output.csv'

# Open the CSV file in write mode
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    header_row = ['List Name', 'Values']
    writer.writerow(header_row)

    # Write the data rows
    for name, values in lists:
        data_row = [name] + values
        writer.writerow(data_row)

print('CSV export completed!')
