# COBS Python Scripts

Here is an implementation of the COBS algorithm from _cmcqueen_'s GitHub implementation found [here](https://github.com/cmcqueen/cobs-python/blob/master/python3/cobs/cobs/_cobs_py.py).

The `encode` and `decode` functions take and return a byte string, i.e. in form `b'  '`, but can easily be altered to accept and return a `bytearray` object instead.

An important note is that there is no delimiter byte added in the `encode` function, but this can be easily added.

There is also test code in the `testCobs.py` file which runs the test data from the [Google doc](https://docs.google.com/document/d/1X5_rWYqVygkXg1IbOM9TwFDC1o-LPYc0QDQILWJRl9Y/edit).