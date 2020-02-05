#!/bin/env python

"""
low-disk-check.py

Copyright 2019-2020  John Begenisich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
from pathlib import Path
import argparse
import configparser
import datetime
import psutil

# psutil.disk_partitions() excludes stuff like /proc, but not /snap
IGNORE_PATHS = ['/snap']


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return '%3.1f %s%s' % (num, unit, suffix)
        num /= 1024.0
    return '%.1f %s%s' % (num, 'Yi', suffix)


def get_xdg(name):
    # returns a Path
    xdg_fallback = {
        'XDG_CONFIG_HOME': Path.home() / '.config',
        'XDG_DATA_HOME': Path.home() / '.local' / 'share',
    }
    path = Path(os.environ[name]) if name in os.environ else xdg_fallback[name]
    return path


def main():
    parser = argparse.ArgumentParser(description='Print alert if disk space is low',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--used', type=int, default=90, metavar='percent',
                        help='Print warning if used%% >= this')
    parser.add_argument('--warn-days', type=int, default=7, metavar='days',
                        help='Only warn if last warning was older than this many days')
    args = parser.parse_args()

    # get config file location
    # config_filename = get_xdg('XDG_CONFIG_HOME') / 'low-disk-check.conf'
    data_filename = get_xdg('XDG_DATA_HOME') / 'low-disk-check.conf'
    data_config = configparser.ConfigParser()
    if data_filename.exists():
        data_config.read(str(data_filename))  # Python < 3.6 requires a str

    partitions = psutil.disk_partitions()
    filesystems_toobig = []
    longest_path = 0
    now = datetime.datetime.now()
    for part in partitions:
        path = part.mountpoint
        if any([path.startswith(ignore) for ignore in IGNORE_PATHS]):
            continue
        usage = psutil.disk_usage(path)
        if usage.percent >= args.used:
            # check if we've warned recently
            if data_config.has_option('mounts', path):
                last_warned = datetime.datetime.fromtimestamp(int(data_config['mounts'][path]))
                if now < last_warned + datetime.timedelta(days=args.warn_days):
                    # don't warn for a while
                    continue
            # write the current time to data config
            if not data_config.has_section('mounts'):
                data_config.add_section('mounts')
            data_config['mounts'][path] = str(int(now.timestamp()))
            # for printing below
            filesystems_toobig.append((path, sizeof_fmt(usage.total), sizeof_fmt(usage.used), usage.percent))
            # keep track of longest path name for formatting below
            if len(path) > longest_path: longest_path = len(path)

    data_filename.parent.mkdir(parents=True, exist_ok=True)
    with open(str(data_filename), 'w') as cf:  # Python < 3.6 requires a str
        data_config.write(cf)

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
