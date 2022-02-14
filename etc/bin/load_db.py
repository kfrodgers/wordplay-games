#
#
#
import os
import glob
from wordle.find_words import FindWords


def main():
    dir_ = os.path.abspath('../data')
    files = glob.glob(dir_ + '/*.txt')

    for f in files:
        print(".. adding words from %s" % f)
        FindWords().load_words(filename=f)


if __name__ == '__main__':
    main()

