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

def main():
    with open('time_elapsed.txt', 'w') as time_file:
        while 1:
            elapsed_time = time.time() - start_time
            time_as_string = convert_to_hours_minutes_secs(int(elapsed_time))
            write_time_to_file(time_file, time_as_string)
            time.sleep(1)

if __name__ == '__main__':
    main()
