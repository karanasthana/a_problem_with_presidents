import csv

def readCSVFile():
    rows = []
    with open("us_prez.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return header, rows

def addNewHeaders(header):
    header.append('year_of_birth')
    header.append('lived_years')
    header.append('lived_months')
    header.append('lived_days')

    return header

def main():
    header, rows = readCSVFile()

    header = addNewHeaders(header)

    # Creating a dictionary to store the indices of the new columns

    headerIndexDict = {}
    i=0
    for (val) in header:
        headerIndexDict[val] = i
        i = i + 1

    print(headerIndexDict)
