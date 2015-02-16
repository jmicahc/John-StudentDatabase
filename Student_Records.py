from collections import OrderedDict

def printline(items, formats):
    '''
    prints a formatted line using the given format strings.
    '''

    for item, Format in zip(items, formats):
        print Format.format(item),
    print ''


def listrows(data, rows):
    '''
    Lists the records in the database corresponding to the
    given rows with dynamically generated white-space
    padding.

    INPUTS:
        - data
           Dictionary with with columns as keys and
           lists of strings as values.
        - rows
           list of ints representing the rows to
           be printed.

    '''
    paddings = ['{:%d}' % (max([len(data[c][r]) 
        for r in rows] + [len(c)]) + 2) for c in data]

    #print headers and rows
    printline(data.keys(), paddings)
    for row in rows:
        items = [data[col][row] for col in data]
        printline(items, paddings)
    return True


def listallrecords(data):
    '''
    Lists all the records in the database.
    Note, this function assumes the inupt 
    dictionary is not empty and each dictionary
    value (list) is of equal length.

    INPUTS:
         - data
            dictionary with columns as keys
            and lists of strings as values.
    OUTPUT:
         - calls listrows on all of the rows.
    '''
    return listrows(data, range(len(data.values()[0])))


def displaybycol(data, col):
    '''
    Asks the user to enter a value for the given column, then
    lists all row numbers matching that value.

    INPUTS:
        - data
            dictionary with columns as keys and lists
            of strings as values
        - col
            the column of *data* that the user is searching.
    OUTPUTS:
        - calls listrows on all the matched rows.
    '''
    rsp = raw_input('Enter %s: ' %(col))
    rows = [i for i, item in enumerate(data[col]) if item == rsp]
    return listrows(data, rows)

def exitprogram(s):
    '''
    Prints a message then returns False. Note,
    the truth value of the return statement 
    determines whether the program should continue.
    '''
    print s
    return False

if __name__ == '__main__':

    # define the column names of the data file.
    colnames = ['First Name', 'Last Name', 'Course Name', 
            'Student ID', 'Date Created']

    # Format the data as a dictionary composed of named columns, where each
    # column is a column in the csv file. One-liner here for the heck of it.
    data = OrderedDict( zip(colnames, [[line.split(',')[i].replace('\n', '') 
        for line in open('Records.txt')] for i in range(len(colnames)) ]))


    # List of all menu options
    menu = [
            '(1) List all student records',
            '(2) Display all records for a specific student ID',
            '(3) Display all records for a specific completed course',
            '(4) Exit the system'
            ]

    # dictionary mapping user repsonses to functions.
    choices = {
        1: listallrecords,
        2: displaybycol,
        3: displaybycol,
        4: exitprogram
        }
    
    #Tuple of all function arugments.
    args = (
        (data,),
        (data, 'Student ID'),
        (data, 'Course Name'),
        tuple(['Have a nice ANCR day!'])
        )


    # main loop.
    cont = True
    while cont:
        try:
            rsp = int(raw_input( '\n'.join(menu) + '\n\nEnter option: ' ))
            if rsp<1 or rsp>4:
                raise ValueError()

            cont = choices[rsp](*args[rsp-1])
        except ValueError:
            print 'invalid input'
            pass
        except Exception:
            print 'Sorry, unknown error occured.'
            raise
