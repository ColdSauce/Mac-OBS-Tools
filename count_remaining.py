import sys
import datetime
from datetime import datetime as dt
import time

def convert_to_hours_minutes_secs(secs):
    mins = int(secs / 60)
    hours = int(mins / 60) % 60 
    secs = secs % 60
    mins = mins % 60
    return "{}:{}:{}".format(str(hours).zfill(2), str(mins).zfill(2), str(secs).zfill(2))

def write_time_to_file(time_file, time_to_write):
    time_file.seek(0)
    time_file.truncate()
    time_file.write(time_to_write)
    time_file.flush()

def start_counting(until_date):
    with open('time_remaining.txt', 'w') as time_file:
        while 1:
            remaining = until_date - datetime.datetime.now()
            time_as_string = convert_to_hours_minutes_secs(int(remaining.seconds))
            write_time_to_file(time_file, time_as_string)
            time.sleep(1)

def main():
    if len(sys.argv) != 2:
        print "Usage: python until.py <a date time>\nExample: python util.py 'Apr 18 2018 4:29PM'"
        return

    arg_date = sys.argv[1]
    datetime_object = dt.strptime(arg_date, '%b %d %Y %I:%M%p')
    start_counting(datetime_object)

if __name__ == '__main__':
    main()
