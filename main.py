import csv
import datetime as dt

from numpy import NaN

headerIndexDict = {}

def readCSVFile():
    rows = []
    with open("us_prez.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    footer = rows[-1]
    rows = rows[:-1]
    return header, rows

def addNewHeaders(header):
    header.append('year_of_birth')
    header.append('lived_years')
    header.append('lived_months')
    header.append('lived_days')

    return header

def cleanup_data(rows):
    dobIndex = headerIndexDict['BIRTH DATE']

    for row in rows:
        dateStr = row[dobIndex]
        dateStrArr = dateStr.split(' ')

        dateStr = dateStrArr[0][:3] + ' ' + dateStrArr[1] + ' ' + dateStrArr[2]
        row[dobIndex] = dateStr

def populate_rows(header, rows):
    # populate columns for headers
    birthDateIndex = headerIndexDict['BIRTH DATE']
    yearBirthIndex = headerIndexDict['year_of_birth']
    print('year birth index is ', yearBirthIndex)
    print(rows[0])

    for row in rows:
        dob = row[birthDateIndex]
        if dob == NaN:
            continue

        row.append(getBirthYear(dob))
        row.append(getLivedYears())
        print(row)

def getBirthYear(dob_str):
    date_time_obj = dt.datetime.strptime(dob_str, '%b %d, %Y')
    dob_year = date_time_obj.year
    return dob_year

def getLivedYears():
    print('test')

def main():
    header, rows = readCSVFile()

    header = addNewHeaders(header)

    # Initializing a dictionary to store the indices of the new columns
    i=0
    for (val) in header:
        headerIndexDict[val] = i
        i = i + 1

    cleanup_data(rows)
    populate_rows(header, rows)

main()