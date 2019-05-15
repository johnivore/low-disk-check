#!/bin/env python

import os
import argparse


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return '%3.1f %s%s' % (num, unit, suffix)
        num /= 1024.0
    return '%.1f %s%s' % (num, 'Yi', suffix)


def filesystem_used_header():
    return '%10s %10s %10s %6s' % ('Filesystem', 'Size', 'Used', 'Used%')


def filesystem_used_string(f):
    return '%-10s %10s %10s %5d%%' % (
        f['filesystem'],
        sizeof_fmt(f['size']),
        sizeof_fmt(f['used']),
        f['percent_used'])


def main():
    parser = argparse.ArgumentParser(description='Alert if disk space is low')
    parser.add_argument('path', nargs='*', default=[])
    parser.add_argument('--used', type=int, default=90, metavar='percent')
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()

    if args.path:
        paths_to_check = args.path
    else:
        paths_to_check = ['/', '/boot', '/home']

    if args.v:
        print('Checking', ' '.join(paths_to_check))

    filesystems_toobig = []
    if args.v:
        print(filesystem_used_header())
    for path in paths_to_check:
        statvfs = os.statvfs(path)
        size = statvfs.f_frsize * statvfs.f_blocks   # size of filesystem
        free = statvfs.f_frsize * statvfs.f_bfree    # actual free bytes
        avail = statvfs.f_frsize * statvfs.f_bavail  # available to users
        used = size - avail
        percent_used = float(used) / float(size) * 100.0  # Python 2, sigh
        f = {'filesystem': path,
             'used': used,
             'size': size,
             'percent_used': int(percent_used)}
        if args.v:
            print(filesystem_used_string(f))
        if percent_used >= args.used:
            filesystems_toobig.append(f)

    if not filesystems_toobig:
        return

    if args.v:
        print()
    print('Alert: the following filesystems are >= %d%% full:\n' % args.used)
    print(filesystem_used_header())
    for f in filesystems_toobig:
        print(filesystem_used_string(f))


# -------------------------------------------------

if __name__ == '__main__':
    main()
