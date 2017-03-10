#!/usr/bin/python
import os
import datetime
import csv
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("path", 
                    help='path to the root project directory'
                    )
parser.add_argument('--exclude',
                    action='append', 
                    default=[],
                    help='directories to be excluded from search'
                    )
parser.add_argument('-v', 
                    '--verbose',
                    action='store_true', 
                    help='verbose mode'
                    )
args = parser.parse_args()


def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total

report_name = 'report-' + args.path.split(os.sep)[::-1][0] + '-' + str(datetime.date.today()) + '.csv'
with open(report_name, 'w') as csvfile:
   
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['directory name',
                       'size',
                       ])

    for entry in os.scandir(args.path):
        if entry.is_dir():
            csvwriter.writerow([entry.path,
                                get_tree_size(entry.path),
                               ])


if args.verbose:
    print('Report saved as ' + report_name)

print("Complete!")
