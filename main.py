import csv
import datetime as dt
import pandas
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from numpy import NaN
from IPython.display import display
from statistics import mode

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
        dobDateStr = row[dobIndex]
        dobDateStrArr = dobDateStr.split(' ')

        dobDateStr = dobDateStrArr[0][:3] + ' ' + dobDateStrArr[1] + ' ' + dobDateStrArr[2]
        row[dobIndex] = dobDateStr

        dodDateStr = row[dodIndex]
        if (dodDateStr != ''):
            dodDateStrArr = dodDateStr.split(' ')

            dodDateStr = dodDateStrArr[0][:3] + ' ' + dodDateStrArr[1] + ' ' + dodDateStrArr[2]
            row[dodIndex] = dodDateStr

def populate_data(header, rows):
    birthDateIndex = headerIndexDict['BIRTH DATE']
    deathDateIndex = headerIndexDict['DEATH DATE']

    livedYearsIndex = headerIndexDict['lived_years']

    for row in rows:
        dob = row[birthDateIndex]
        dob_dt_obj = dt.datetime.strptime(dob, '%b %d, %Y')
        if dob == NaN:
            continue

        dod = row[deathDateIndex]
        dod_dt_obj = ''
        if dod != '':
            dod_dt_obj = dt.datetime.strptime(dod, '%b %d, %Y')


        row.append(getBirthYear(dob_dt_obj))
        row.append(getLivedYears(dob_dt_obj, dod_dt_obj))
        row.append(getLivedMonths(dob_dt_obj, dod_dt_obj, row[livedYearsIndex]))
        row.append(getLivedDays(dob_dt_obj, dod_dt_obj))
    
    return rows

def getBirthYear(dob_dt_obj):
    dob_year = dob_dt_obj.year
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

def prettyPrintPrezList(header, list):
    list.insert(0, header)
    df = pandas.DataFrame(list[:11])
    display(df)

def calcMean(list):
    count=0
    total=0
    livedDaysIndex = headerIndexDict['lived_days']

    for row in list:
        total = total + row[livedDaysIndex]
        count = count + 1

    return (total/count)

def calcWeightedMean(list):
    count = 0
    total = 0
    weight = (1/len(list))
    livedDaysIndex = headerIndexDict['lived_days']

    for row in list:
        total = total + (row[livedDaysIndex] * weight)
        count = count + (weight)

    return (total/count)

def calcMedian(list):
    print("test Median")
    display(pandas.DataFrame(list))

    # Sorting the list as per ascending order of number of days lived
    list2 = sorted(list, key=itemgetter(headerIndexDict['lived_days']))

    for row in list2:
        print(row)

    length = len(list2)

    medianEl1 = 0
    medianEl2 = 0
    if length % 2 == 1:
        medianEl1 = (int)((length + 1) / 2)
        medianEl2 = (int)((length + 1) / 2)
    else:
        medianEl1 = ((int)(length/2))
        medianEl2 = (((int)(length/2) + 1))

    val1 = list2[medianEl1][headerIndexDict['lived_days']]
    val2 = list2[medianEl2][headerIndexDict['lived_days']]

    median = (val1 + val2) / 2
    
    print('median days lived', median)
    return median

def calcMode(list):
    listDays = []
    for row in list:
        listDays.append(row[headerIndexDict['lived_days']])

    modeVal = mode(listDays)
    print('Mode is - ', modeVal)
    print('** Mode prints the highest occuring value, if all are distinct, it selects the first values as puts that up as the mode **')
    return modeVal
    

def calcMax(list):
    livedDaysIndex = headerIndexDict['lived_days']
    max = list[0][livedDaysIndex]
    for row in list:
        livedDays = row[livedDaysIndex]
        if (livedDays > max) :
            max = livedDays
    print("Maximum ", max)
    return max

def calcMin(list):
    livedDaysIndex = headerIndexDict['lived_days']
    min = list[0][livedDaysIndex]
    for row in list:
        livedDays = row[livedDaysIndex]
        if (livedDays < min) :
            min = livedDays
    print("Minimum ", min)
    return min

def prettyPrintStatistics(mean, weighted_mean, median, mode, max, min):
    list = []
    list.append(['Mean', mean])
    list.append(['Weighted Mean', weighted_mean])
    list.append(['Median', median])
    list.append(['Mode', mode])
    list.append(['Max', max])
    list.append(['Min', min])

    df = pandas.DataFrame(list)
    pandas.set_option("precision", 3)

    display(df)

def main():
    header, rows = readCSVFile()

    header = addNewHeaders(header)

    # Initializing dictionary to store the indices of the new columns
    i=0
    for (val) in header:
        headerIndexDict[val] = i
        i = i + 1

    cleanup_data(rows)
    rows = populate_data(header, rows)

    leastLivedPrez = sorted(rows, key=itemgetter(headerIndexDict['lived_days']))
    print('Least Lived Presidents')
    prettyPrintPrezList(header, leastLivedPrez)
    print('\n')
    
    mostLivedPrez = sorted(rows, key=itemgetter(headerIndexDict['lived_days']), reverse=True)
    print('Most Lived Presidents')
    prettyPrintPrezList(header, mostLivedPrez)

    mean = calcMean(rows)
    weighted_mean = calcWeightedMean(rows)
    median = calcMedian(rows)
    mode = calcMode(rows)
    max = calcMax(rows)
    min = calcMin(rows)
    prettyPrintStatistics(mean, weighted_mean, median, mode, max, min)
    

main()