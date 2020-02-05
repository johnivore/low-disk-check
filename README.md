# low-disk-check

## About

Prints an alert if low on disk space on any mounted partition.

For each mountpoint, it keeps track of when the last warning was issued, and won't warn again for a while.


## Requirements

* Python 3.5+
* psutil (See "pre-psutil" branch for a version that doesn't require psutil)


## License

```
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
```
