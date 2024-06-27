# encoding=utf8
from util import *


if __name__ == '__main__':
    f = "count.txt"
    key = "test1"
    i = file_get(f, key)
    file_put(f, key, i+10)
    print(file_get(f, key))
