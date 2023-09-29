# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    reformated_dates = [datetime.strptime(old_dt, "%Y-%m-%d").strftime('%d %b %Y') for old_dt in old_dates]
    return reformated_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    output_list = []
    frmat = datetime.strptime(start, '%Y-%m-%d')
    for a in range(n):
        output_list.append(frmat + timedelta(days=a))
    return output_list

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_range_len = date_range(start_date, len(values))
    zipped_list = list(zip(date_range_len, values))
    return zipped_list


def helper(infile):
    
    headSet = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    with open(infile, 'r') as f:
        c = DictReader(f, fieldnames=headSet)
        all_rows = [row for row in c]

        all_rows.pop(0)
    
    return all_rows

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    
    rqrd_format = '%m/%d/%Y'
    rows = helper(infile)
    dict_for_latefee = defaultdict(float)

    for row in rows:
       
        patron = row['patron_id']
        due_on = datetime.strptime(row['date_due'], rqrd_format)
        returned_on = datetime.strptime(row['date_returned'], rqrd_format)

        late_days = (returned_on - due_on).days

        dict_for_latefee[patron]+= 0.25 * late_days if late_days > 0 else 0.0

    header = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in dict_for_latefee.items()
    ]

    with open(outfile, 'w') as wrt:
        dcrr = DictWriter(wrt, ['patron_id', 'late_fees'])
        dcrr.writeheader()
        dcrr.writerows(header)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
