import sys
import os
import re

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 4:
        print """
Usage:

%s find replace filename.txt [filename2.txt...]
""" % argv[0]
        exit

    find = argv[1]
    replace = argv[2]
    filepaths = argv[3:]

    for filepath in filepaths:
        text = open(filepath).read()
        #print re.sub(find, replace, text)
        new_text = re.sub(find, replace, text)
        if new_text != text:
            print filepath
            open(filepath, 'w').write(new_text)

if __name__ == '__main__':
    main()