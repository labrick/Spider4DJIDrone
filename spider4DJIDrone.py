#!/usr/bin/python3

import sys
import getopt
import time

from sqliteWrapper import SqliteWrapper
from updateData import updateData
from analyseData import getResult
from drawPic import plotBar,plotPie
def usage():
    str = \
'''usage: spider4DJIDrone [option] ... [-p period [startDate1 startDate2 startDate3] | -m months ] [arg] ...
Options and arguments (and corresponding environment variables):
    -h display this help document
    -p the time period of data analyzed
    -u update data only[default]'''
    print(str)

def checkDateValidation(period, months):
    if type(period) != type(1):
        print('invalid type for period parameter')
        sys.exit()
    if len(months) > 3:
        print("Too many months!!!")
        sys.exit()
    num = len(months)
    for i in range(num):
        if type(months[i]) != type('abc'):
            print("Invalid type for months parameter")
            sys.exit()
        date = months[i]
        if len(date) != 6 or (date.isdigit() == False):
            print("Invalid Date Input : You should input right digital characters")
            sys.exit()
        month = int(date[4:6]);
        if month <=0 or month >=13:
            print("Invalid Date Input: Please check the month")
            sys.exit()

def subMonth(year, month, sub):
    month = month - sub
    if month <= 0:
        month += 12
        year -= 1
    return year, month

def getDefaultParam():
    period = 2
    tstruct = time.localtime(time.time())
    year = tstruct.tm_year
    month = tstruct.tm_mon
    year1, month1 = subMonth(year, month, 6)
    year2, month2 = subMonth(year, month, 4)
    year3, month3 = subMonth(year, month, 2)
    months = [str(year1) + str(month1), str(year2) + str(month2), str(year3) + str(month3)]
    # print(months)
    return period, months


def main():
    sqliteWrapper = SqliteWrapper("C222")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:u")
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    period, months = getDefaultParam()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt == '-p':
            period = int(arg)
            months = args
        elif opt == '-u':
            print("updating data...")
            updateData(sqliteWrapper)
            sys.exit(0)

    print("updating data...")
    updateData(sqliteWrapper)
    print("update data ok!")
    # # to analyse the requst data , need parameter 'period' and 'months'
    # checkDateValidation(period, months)
    print("analyzing data...")
    nameList, valueList = getResult(period, months)
    print("analyze data ok!")
    plotBar(nameList, valueList, period, months)
    plotPie(nameList, valueList[0], months[0])
    print("plot bar and pie ok!")

if __name__ == '__main__':
    main()
