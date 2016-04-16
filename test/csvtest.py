import csv

with open('test.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
    for row in spamreader:
        print(row)
