import csv
import datetime as dt
from dateutil.relativedelta import relativedelta

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
    dodIndex = headerIndexDict['DEATH DATE']

    for row in rows:
        print(row[0])
        dobDateStr = row[dobIndex]
        dobDateStrArr = dobDateStr.split(' ')

        dobDateStr = dobDateStrArr[0][:3] + ' ' + dobDateStrArr[1] + ' ' + dobDateStrArr[2]
        row[dobIndex] = dobDateStr

        dodDateStr = row[dodIndex]
        print(dodDateStr)
        if (dodDateStr != ''):
            dodDateStrArr = dodDateStr.split(' ')

            print(dodDateStrArr)
            dodDateStr = dodDateStrArr[0][:3] + ' ' + dodDateStrArr[1] + ' ' + dodDateStrArr[2]
            row[dodIndex] = dodDateStr
        print('\n')

def populate_rows(header, rows):
    # populate columns for headers
    birthDateIndex = headerIndexDict['BIRTH DATE']
    deathDateIndex = headerIndexDict['DEATH DATE']
    yearBirthIndex = headerIndexDict['year_of_birth']
    livedYearsIndex = headerIndexDict['lived_years']
    livedMonthsIndex = headerIndexDict['lived_months']

    print('year birth index is ', yearBirthIndex)
    print(rows[0])

    for row in rows:
        dob = row[birthDateIndex]
        dod = row[deathDateIndex]
        if dob == NaN:
            continue

        row.append(getBirthYear(dob))

        dob_dt_obj = dt.datetime.strptime(dob, '%b %d, %Y')
        dod_dt_obj = ''
        if dod != '':
            dod_dt_obj = dt.datetime.strptime(dod, '%b %d, %Y')

        row.append(getLivedYears(dob_dt_obj, dod_dt_obj))
        row.append(getLivedMonths(dob_dt_obj, dod_dt_obj, row[livedYearsIndex]))
        row.append(getLivedDays(dob_dt_obj, dod_dt_obj))
        print(row)

def getBirthYear(dob_str):
    date_time_obj = dt.datetime.strptime(dob_str, '%b %d, %Y')
    dob_year = date_time_obj.year
    return dob_year

def getLivedYears(dob_obj, dod_obj):
    effective_dod_obj = dod_obj
    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')
    
    return (relativedelta(effective_dod_obj, dob_obj).years)

def getLivedMonths(dob_obj, dod_obj, total_years):
    effective_dod_obj = dod_obj
    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')
    
    return (relativedelta(effective_dod_obj, dob_obj).months + (total_years * 12))


def getLivedDays(dob_obj, dod_obj):
    effective_dod_obj = dod_obj
    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')
    
    date_format = "%m/%d/%Y"
    a = dt.datetime.strftime(effective_dod_obj, date_format)
    a = dt.datetime.strptime(a, '%m/%d/%Y').date()
    b = dt.datetime.strftime(dob_obj, date_format)
    b = dt.datetime.strptime(b, '%m/%d/%Y').date()
    
    return ((a-b).days)

    



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