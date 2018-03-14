#!/usr/bin/python3

import sys
import getopt

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

def main():

    try:
        opts, args = getopt.getopt(sys.argv, "hpu",["period="])
    except getopt.GetoptError:
        print("spider4DJIDrone.py -p <period> month1 month2 month3")
        sys.exit(2)

    sqliteWrapper = SqliteWrapper("C222")
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt == '-p':
            print("updating data...")
            updateData(sqliteWrapper)

            print("analizing data...")
            getResult(sys.argv)
        elif opt == '-u':
            print("updating data...")
            updateData(sqliteWrapper)

    print("updating data...")
    updateData(sqliteWrapper)
    argv = []
    #argv.append('')
    argv.append('-p')
    argv.append('2')
    argv.append('201706')
    argv.append('201707')
    argv.append('201708')

    # to analyse the requst data , need parameter 'period' and 'months'
    period = 2
    months = ['201706', '201708','201710']
    checkDateValidation(period,months)
    nameList, valueList = getResult(period, months)
    plotBar(nameList, valueList,months)
    plotPie(nameList, valueList[0],months[0])

if __name__ == '__main__':
    main()
