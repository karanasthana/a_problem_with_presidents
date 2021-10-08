import csv
import pandas
import datetime as dt
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from numpy import NaN
from IPython.display import display
from statistics import mode

headerIndexDict = {}
spacedDateFormat = '%b %d, %Y'
slashedDateFormat = '%m/%d/%Y'

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

    # Converting all 4 lettered months into consistent 3 lettered months (e.g. July to Jul & June to Jun)
    for row in rows:
        dobDateStr = row[dobIndex]
        dobDateStrArr = dobDateStr.split(' ')

        dobDateStr = '{} {} {}'.format(dobDateStrArr[0][:3], dobDateStrArr[1], dobDateStrArr[2])
        row[dobIndex] = dobDateStr

        dodDateStr = row[dodIndex]
        if (dodDateStr != ''):
            dodDateStrArr = dodDateStr.split(' ')

            dodDateStr = '{} {} {}'.format(dodDateStrArr[0][:3], dodDateStrArr[1], dodDateStrArr[2])
            row[dodIndex] = dodDateStr

def populate_data(header, rows):
    birthDateIndex = headerIndexDict['BIRTH DATE']
    deathDateIndex = headerIndexDict['DEATH DATE']
    livedYearsIndex = headerIndexDict['lived_years']

    for row in rows:
        dob = row[birthDateIndex]
        dob_dt_obj = dt.datetime.strptime(dob, spacedDateFormat)
        if dob == NaN:
            continue

        dod = row[deathDateIndex]
        dod_dt_obj = ''
        if dod != '':
            dod_dt_obj = dt.datetime.strptime(dod, spacedDateFormat)


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
        today_str = dt.datetime.strftime(dt.date.today(), spacedDateFormat)
        effective_dod_obj = dt.datetime.strptime(today_str, spacedDateFormat)
    
    return (relativedelta(effective_dod_obj, dob_obj).years)

def getLivedMonths(dob_obj, dod_obj, total_years):
    effective_dod_obj = dod_obj

    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), spacedDateFormat)
        effective_dod_obj = dt.datetime.strptime(today_str, spacedDateFormat)
    
    return (relativedelta(effective_dod_obj, dob_obj).months + (total_years * 12))


def getLivedDays(dob_obj, dod_obj):
    effective_dod_obj = dod_obj
    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), spacedDateFormat)
        effective_dod_obj = dt.datetime.strptime(today_str, spacedDateFormat)

    date_format = slashedDateFormat
    a = dt.datetime.strftime(effective_dod_obj, date_format)
    a = dt.datetime.strptime(a, date_format).date()
    b = dt.datetime.strftime(dob_obj, date_format)
    b = dt.datetime.strptime(b, date_format).date()

    return ((a-b).days)

def prettyPrintPrezList(header, list):
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    list.insert(0, header)
    df = pandas.DataFrame(list[1:11], columns=header)

    ax.table(cellText=df.values, colLabels=df.columns, colColours=(['lightblue'] * len(header)))
    fig.tight_layout()
    plt.show()


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

    # print('Mean is - ', (total/count))
    return (total/count)

def calcMedian(list):
    display(pandas.DataFrame(list))

    # Sorting the list as per ascending order of number of days lived
    list2 = sorted(list, key=itemgetter(headerIndexDict['lived_days']))
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
    # print('Median is - ', median)
    return median

def calcMode(list):
    listDays = []
    for row in list:
        listDays.append(row[headerIndexDict['lived_days']])

    modeVal = mode(listDays)
    # print('Mode is - ', modeVal)
    print('** Mode prints the highest occuring value, if all are distinct, it selects the first values as puts that up as the mode **')
    return modeVal
    

def calcMax(list):
    livedDaysIndex = headerIndexDict['lived_days']
    max = list[0][livedDaysIndex]
    for row in list:
        livedDays = row[livedDaysIndex]
        if (livedDays > max) :
            max = livedDays
    # print("Maximum ", max)
    return max

def calcMin(list):
    livedDaysIndex = headerIndexDict['lived_days']
    min = list[0][livedDaysIndex]
    for row in list:
        livedDays = row[livedDaysIndex]
        if (livedDays < min) :
            min = livedDays
    # print("Minimum ", min)
    return min

def calcSD(list):
    livedDaysIndex = headerIndexDict['lived_days']
    mean = calcMean(list)

    sigmaVal = 0;
    for row in list:
        sigmaVal = sigmaVal + ((row[livedDaysIndex] - mean) ** 2)
    
    before_root_val = sigmaVal / (len(list) - 1)
    standard_deviation = (before_root_val ** 0.5)
    # print('Standard Deviation ', standard_deviation)
    return standard_deviation

def prettyPrintStatistics(mean, weighted_mean, median, mode, max, min, standard_deviation):
    list = []
    list.append(['Mean', mean])
    list.append(['Weighted Mean', weighted_mean])
    list.append(['Median', median])
    list.append(['Mode', mode])
    list.append(['Max', max])
    list.append(['Min', min])
    list.append(['Standard Deviation', standard_deviation])

    # df = pandas.DataFrame(list)
    # pandas.set_option("precision", 3)

    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    list.insert(0, ['Type', 'Value'])
    df = pandas.DataFrame(list[1:], columns=list[0])

    ax.table(cellText=df.values, colLabels=df.columns, colColours=(['lightblue'] * 2))
    fig.tight_layout()
    plt.show()

def showDataOnGraph(rows):
    tlist = list(zip(*rows))
    xaxis = tlist[0]
    yaxis = tlist[8]

    # computations to fetch the values of statistical data
    num_rows = len(rows)
    mean_value = calcMean(rows)
    median_value = calcMedian(rows)
    mode_value = calcMode(rows)
    max_value = calcMax(rows)
    min_value = calcMin(rows)
    sd_value = calcSD(rows)

    # temporary computations to create list equal to the computed values
    y_mean = [mean_value] * num_rows
    y_median = [median_value] * num_rows
    y_mode = [mode_value] * num_rows
    y_max = [max_value] * num_rows
    y_min = [min_value] * num_rows
    y_sd_max = [mean_value + sd_value] * num_rows
    y_sd_min = [mean_value - sd_value] * num_rows

    # gca is used to Get the Current Axis
    ax = plt.gca()
    
    # Rotating the X-axis values by 90 to make them visible
    ax.tick_params(axis='x', labelrotation = 90)

    mean_line = ax.plot(xaxis, y_mean, label='Mean - ' + str(format(mean_value, ".3f")), linestyle='--')
    median_line = ax.plot(xaxis, y_median, label='Median - ' + str(median_value), linestyle=':')
    mode_line = ax.plot(xaxis, y_mode, label='Mode - ' + str(mode_value), linestyle='-')
    max_line = ax.plot(xaxis, y_max, label='Max - ' + str(max_value), linestyle='dotted')
    min_line = ax.plot(xaxis, y_min, label='Min - ' + str(min_value), linestyle='dotted')
    # sd_max_line = ax.plot(xaxis, y_sd_max, label='Standard Deviation (+ve)', linestyle='-.')
    # sd_min_line = ax.plot(xaxis, y_sd_min, label='Standard Deviation (-ve)', linestyle='-.')

    # Filling color between the two values of Standard Deviation
    ax.fill_between(xaxis, y_sd_min, y_sd_max, color='blue', alpha=0.15, label='Standard Deviation')

    legend = ax.legend(loc='lower left')

    plt.plot(xaxis, yaxis)
    plt.show()

def main():
    header, rows = readCSVFile()

    header = addNewHeaders(header)

    # Initializing dictionary to store the indices of the new columns
    i=0
    for val in header:
        headerIndexDict[val] = i
        i = i + 1

    cleanup_data(rows)
    rows = populate_data(header, rows)

    leastLivedPrez = sorted(rows, key=itemgetter(headerIndexDict['lived_days']))
    # print('Least Lived Presidents')
    prettyPrintPrezList(header, leastLivedPrez)
    # print('\n')
    
    mostLivedPrez = sorted(rows, key=itemgetter(headerIndexDict['lived_days']), reverse=True)
    # print('Most Lived Presidents')
    prettyPrintPrezList(header, mostLivedPrez)

    mean = calcMean(rows)
    weighted_mean = calcWeightedMean(rows)
    median = calcMedian(rows)
    mode = calcMode(rows)
    max = calcMax(rows)
    min = calcMin(rows)
    standard_deviation = calcSD(rows)
    prettyPrintStatistics(mean, weighted_mean, median, mode, max, min, standard_deviation)
    
    showDataOnGraph(rows)

main()