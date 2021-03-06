import csv
import glob
import os
from os.path import dirname


def collect_records(file_path_list):
    full_data_rows_list = []

    # for every filepath in the file path list
    for f in file_path_list:
        # reading the csv file
        with open(f, 'r', encoding='utf8', newline='') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            # skip header row
            next(csvreader)

            # extracting each data row one by one and append it
            for line in csvreader:
                # print(line)
                full_data_rows_list.append(line)

    return full_data_rows_list


def collect_files(filepath):
    file_path_list = []

    # collect each filepath
    for root, dirs, files in os.walk(filepath):
        # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root, '*'))

    return file_path_list


def create_output_file(full_data_rows_list):
    # creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
    # Apache Cassandra tables

    if os.path.exists('event_datafile_new.csv'): 
        os.remove('event_datafile_new.csv')

    output_row_count = 0
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open('event_datafile_new.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist', 'firstName', 'gender', 'itemInSession', 'lastName', 'length', \
                         'level', 'location', 'sessionId', 'song', 'userId'])
        for row in full_data_rows_list:
            if row[0] == '':
                continue
            output_row_count += 1
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))

    return output_row_count


def main():
    # get the current folder and subfolder event data
    filepath = 'event_data'
    # print(filepath)

    file_path_list = collect_files(filepath)
    # print(file_path_list)
    full_data_rows_list = collect_records(file_path_list)
    output_row_count = create_output_file(full_data_rows_list)

    print(f'Written {output_row_count} rows to the output file.')


if __name__ == '__main__':
    main()
