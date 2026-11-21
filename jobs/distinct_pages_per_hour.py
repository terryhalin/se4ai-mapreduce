"""Task 3: how many DIFFERENT pages were requested in each hour?

A colleague wrote this job and says it works. It counts, for every hour of the
day, how many distinct HTML pages (paths ending in ``.html``) were requested
at least once in that hour.

Run it twice and compare:

    python3 run_job.py distinct_pages_per_hour --workers 1
    python3 run_job.py distinct_pages_per_hour --workers 4

Then fix it (see the README). Test it:
    python3 -m pytest tests/test_distinct_pages_per_hour.py
"""

from mapreduce import parse_line

SORT_BY = "key"


def mapper(line):
    request = parse_line(line)
    if request is None or not request["path"].lower().endswith(".html"):
        return
    yield request["hour"], request["path"]


def reducer(key, values):
    return len(set(values))
