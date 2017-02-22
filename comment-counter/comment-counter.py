#!/usr/bin/python
import os
import datetime
import csv
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("path", 
                    help='absolute path to the root project directory'
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


report_name = 'report-' + args.path.split(os.sep)[::-1][0] + '-' + str(datetime.date.today()) + '.csv'
with open(report_name, 'w') as csvfile:
   
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['file name', 
                       'total lines',
                       'comment lines',
                       'effective lines',
                       'blank lines', 
                       'comment percentage',
                       'code percentage'
                       ])
    
    total_row, total_code, total_comment, total_blank = 0, 0, 0, 0
    for (root, dirs, files) in os.walk(args.path):
        
        dirs[:] = [d for d in dirs if d not in args.exclude]
        files[:] = [f for f in files if f.endswith('.h') or f.endswith('.cpp')]
        
        for file_name in files:                
            with open(os.path.join(root, file_name), 'r') as f:
                
                if args.verbose:
                    print('reading ' + file_name)
                
                rel_dir = os.path.relpath(root, args.path)
                name = file_name
                
                if rel_dir != '.':
                    name = os.path.join(rel_dir, file_name)
                
                count_row, count_code, count_comment, count_blank = 0, 0, 0, 0
                multiline_comment = False                
                for row in f:
                    
                    count_row += 1
                    clean_row = row.strip()
                    
                    if multiline_comment:
                        count_comment += 1
                    elif not clean_row:
                        count_blank += 1
                    elif clean_row.startswith('//'):
                        count_comment += 1
                    elif clean_row.startswith('/*') and '*/' not in clean_row:
                        count_comment += 1
                        multiline_comment = True
                    elif clean_row.endswith('*/'):
                        count_comment += 1
                        multiline_comment = False
                    else:
                        count_code += 1
                
                try:
                
                    csvwriter.writerow([name, 
                                        count_row, 
                                        count_comment, 
                                        count_code, 
                                        count_blank, 
                                        100 * (count_comment/count_row), 
                                        100 * (count_code/count_row)
                                        ])
                
                except(ZeroDivisionError):
                
                    csvwriter.writerow([name, 
                                        0, 
                                        0, 
                                        0, 
                                        0, 
                                        0, 
                                        0
                                        ])
                                    
                total_row += count_row
                total_comment += count_comment
                total_code += count_code
                total_blank += count_blank
    
    csvwriter.writerow(['Total',
                        total_row,
                        total_comment,
                        total_code,
                        total_blank,
                        100 * (total_comment/total_row), 
                        100 * (total_code/total_row)
                        ])

if args.verbose:
    print('Report saved as ' + report_name)

print("Complete!")

