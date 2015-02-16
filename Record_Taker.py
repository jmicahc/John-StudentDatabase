import sys
import re
from collections import OrderedDict
from datetime import datetime

class CSVPrinter():
    '''
    Class for writing to a csv file.
    '''
    def __init__(self, filename):
        self.path = filename
        self.datafile = open(filename, 'a')
    
    def csvLine(self, items):
        for item in items[:-1]:
            self.datafile.write(str(item) + ",")
        if not items == []:
            self.datafile.write(str(items[-1]))
        self.datafile.write('\n')


def parsedate(string):
    '''
    Tests whether the input string match is a DD/MM/YYYY regex string.
    If the test fails, a ValueError is raised.

    ***Note*** this is very imperfect. Really should use a datetime
    object, but that object can't reprepresent date as DD/MM/YYYY.
    The current regex matches illegal dates, such as 99/99/9999.
    I'm not sure how to catch all the illegal dates with a regex,
    especially since legal days are dependent on the month.

    INPUT:
        - string
           string to represent a date formatted as
           DD/MM/YYYY.
    OUTPUT:
        - string
           Same string as the input string. Returned only if
           the string matches a regex string. Otherwise, a
           value error is returned.
    '''
    regex = re.compile('\d{2}[-/]\d{2}[-/]\d{4}')
    legals = regex.findall(string)
    if len(legals)==1:
        return string
    raise ValueError()


def fillform(fields):
    '''
    Populates a dictionary with user inputs.

    INPUT: 
        - fields
           A dictionary with field names as keys and 
           and functions for processing the raw input 
           as values.
    OUTPUT:
        - user 
           A dicitonary with field nams as keys and
           the processed user input as fields.
    '''
    user = OrderedDict([])
    for field in fields:
        while True:
            try:
                user[field] = fields[field](raw_input(field + ": "))
            except ValueError as e:
                # temporary solution. We should define an error class for the form.
                if field == 'Student ID':
                    print "Input should be a number"
                elif field == 'Date Completed':
                    print 'Input must be formatted "MM/DD/YYYY"'
                continue
            break
    return user

if __name__ == "__main__":

    #define field names as keys and input constraints as values.
    fields = OrderedDict([
        ("First Name", str), 
        ("Last Name", str), 
        ("Course Name", str),
        ('Student ID', int), 
        ('Date Completed', parsedate)
        ])

    # Create a printing object for writing to csv file.
    printer = CSVPrinter('Records.txt')


    cont = True
    while cont:
        user = fillform(fields)
        printer.csvLine(user.values())
        cont = raw_input('conitnue (y/n): ') == 'y'

    print 'Have a great day!'
