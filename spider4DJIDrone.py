#!/usr/bin/python3

import sys
import getopt

from sqliteWrapper import SqliteWrapper
from updateData import updateData
from analyseData import getResult

def usage():
    str = \
'''usage: spider4DJIDrone [option] ... [-p period [startDate1 startDate2 startDate3] | -m months ] [arg] ...
Options and arguments (and corresponding environment variables):
    -h display this help document
    -p the time period of data analyzed
    -u update data only[default]'''
    print(str)


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
    argv.append('')
    argv.append('-p')
    argv.append('2')
    argv.append('201801')
    argv.append('201802')
    argv.append('201803')
    getResult(argv)

if __name__ == '__main__':
    main()
