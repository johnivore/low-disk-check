# low-disk-check

## About

Prints an alert if low on disk space on any mounted partition.

For each mountpoint, it keeps track of when the last warning was issued, and won't warn again for a while.


## Requirements

* Python 3.5+
* psutil (See "pre-psutil" branch for a version that doesn't require psutil)
