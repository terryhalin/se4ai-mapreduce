"""Task 1: how many times was each image viewed?

Count successful views of every image on the NASA web server, like the
"count views per photo" example in the lecture.

A request counts as a view of an image when ALL of these hold:
  * the line can be parsed (``parse_line`` does not return ``None``);
  * the method is ``"GET"``;
  * the status is ``200`` (OK);
  * the path ends in ``.gif``, ``.jpg`` or ``.jpeg``, in ANY letter case:
    ``/images/KSC-logosmall.gif`` counts, and so does the Apollo 13 photo
    ``/history/apollo/apollo-13/images/70HC314.GIF``.

Status 304 ("Not Modified") means the browser already had the image in its
cache and the server did not send it again: that is not a view here.

Run it:  python3 run_job.py views_per_image
Test it: python3 -m pytest tests/test_views_per_image.py
"""

from mapreduce import parse_line

IMAGE_EXTENSIONS = (".gif", ".jpg", ".jpeg")


def mapper(line):
    """Turn ONE log line into zero or more (key, value) pairs.

    Yield ``(path, 1)`` if the line is a view of an image; yield nothing
    otherwise. Look at one line only: no global variables.
    """
    request = parse_line(line)
    if request is None:
        return
    if request["method"] != "GET" or request["status"] != 200:
        return
    if not request["path"].lower().endswith(IMAGE_EXTENSIONS):
        return
    yield request["path"], 1


def reducer(key, values):
    """Combine ALL values for one key into one result.

    ``key`` is an image path, ``values`` is a list such as ``[1, 1, 1]``.
    Return the total number of views of that image.
    """
    return sum(values)
