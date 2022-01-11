import os
import errno


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def asarray(v):
    return [s.strip() for s in v.split(',')]
