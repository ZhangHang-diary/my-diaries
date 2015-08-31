
str.endswith(suffi[, strat[, end]])
"""
Return True if the string ends with the specified suffix. otherwise return False. suffix can also be a tuple of suffixes to look for. With optional start, test beginning at that position. With optional end, stop comparing at that position.
"""


urllib.unquote(path)
"""
Replace %xx escapes by their single-character equivalent.
EXAMPLE: 
>>> urllib.unquote("/%7Econnolly/")
("/~connolly/")
"""

>>> urllib.quote("/~what/")
'/%7Ewhat/'


posixpath.normpath(path)
"""- posixpath for UNIX-style paths
   - ntpath for Windows paths
   - macpath for old-style MacOS paths
   - os2emxpath for OS/2 EMX paths
Normalize a pathname by collapsing redundant separators and up-level references
so that A//B, A/B/, A/./B and A/foo/../B all become A/B. 
This string manipulation may change the meaning of a path that 
contains symbolic links. On Windows, it converts forward slashes to backward slashes. 
To normalize case, use normcase().
"""


os.path.splitdrive(path)
"""Split the pathname path into a pair (drive, tail) where drive is either 
a drive specification or the empty string. On systems which 
do not use drive specifications, drive will always be the empty string. 
In all case, drive + tail will be the same as path.
"""


os.curdir
"""
The constant string used by the operating system to refer to the current directory. This is '.' for Windows and POSIX. Also available via os.path.
"""


os.pardir
"""
The constant string used by the operating system to refer to the parent directory. This is '..' for Windows and POSIX. Also available via os.path.
"""

os.listdir(path)
"""
Return a list containing the names of the entries in the directory given by path. The list is in arbitrary order. It does not include the special entries '.' and '..' even if they are present in the directory.

Availability: Unix, Windows.

Changed in version 2.3: On Windows NT/2k/XP and Unix, if path is a Unicode object, the result will be a list of Unicode objects. Undecodable filenames will still be returned as string objects.
"""
_______________________________________________________________________________________________

>>> for x in range(1,11):
...     if x % 2 == 0:
...             continue
...     print x
... 
1 3 5 7 9
_______________________________________________________________________________________________

>>> filter(lambda x: x%2 != 0, xrange(1,101))
[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99]
>>> filter(None, [1,None,2,3])
[1, 2, 3]
__________________________________________________________________________________________

import os
import posixpath
import urllib

def translate_path(path):
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        print words
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

if __name__ == '__main__':
    print translate_path("/../what/abc")
_____________________________________________________________________________________________

seq.sort([function])

list.sort(key=lambda a: a.lower())

______________________________________________________________________________________________

>>> cgi.escape("<")
'&lt;'
______________________________________________________________________________________________



























