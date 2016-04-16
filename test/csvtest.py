import csv

intl = []
floatl = []

with open('test.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
    for row in spamreader:
        intl.append(int(row[0]))
        floatl.append(row[1])

print(intl)
print(floatl)
