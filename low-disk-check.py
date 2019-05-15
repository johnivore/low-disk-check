#!/bin/env python

import argparse
import psutil


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return '%3.1f %s%s' % (num, unit, suffix)
        num /= 1024.0
    return '%.1f %s%s' % (num, 'Yi', suffix)


def filesystem_used_header():
    return


def main():
    parser = argparse.ArgumentParser(description='Print an alert if disk space is low')
    parser.add_argument('--used', type=int, default=90, metavar='percent')
    args = parser.parse_args()

    partitions = psutil.disk_partitions()
    filesystems_toobig = []
    longest_path = 0
    for part in partitions:
        path = part.mountpoint
        usage = psutil.disk_usage(path)
        if usage.percent >= args.used:
            filesystems_toobig.append((path, sizeof_fmt(usage.total), sizeof_fmt(usage.used), usage.percent))
            if len(path) > longest_path: longest_path = len(path)

    if not filesystems_toobig:
        return

    longest_path = max(len('Filesystem'), longest_path)
    print('Alert: the following filesystems are >= %d%% full:\n' % args.used)
    print('%-*s %10s %10s %6s' % (longest_path, 'Filesystem', 'Size', 'Used', 'Used%'))
    for path, size, used, percent in filesystems_toobig:
        print('%-*s %10s %10s %5d%%' % (longest_path, path, size, used, percent))


# -------------------------------------------------

if __name__ == '__main__':
    main()
