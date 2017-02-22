# scripts

This is a grand collection consisting of one whole script written for personal use. 

# comment-counter.py

The comment-counter script reads a specified directory and subdirectories looking for for C/C++ source and header files (specifically .cpp and .h), counts the number of efective code lines, comment lines and blank lines. It generates a report formatted as CSV that shows the total lines of code, number of comment lines, effective code lines, blank lines as well as percentage of comment and code lines for each file read as well the project in total. It is Python 2/3 compatible.

Usage: 
```
comment-counter.py [-h] [--exclude EXCLUDE] [-v] path

positional arguments:
  path               path to the root project directory

optional arguments:
  -h, --help         show this help message and exit
  --exclude EXCLUDE  directories to be excluded from search
  -v, --verbose      verbose mode
```

