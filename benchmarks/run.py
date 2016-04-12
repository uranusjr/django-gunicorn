import statistics
import timeit


setup_code = """
import atexit
import requests
import subprocess
import sys
import time

from __main__ import test_runserver

p = subprocess.Popen(
    [sys.executable, 'simpledjango/manage.py', {cmd!r}],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
atexit.register(lambda: p.terminate())
time.sleep(1)   # Wait for the server to launch.
"""


def test_runserver():
    import requests
    requests.get('http://localhost:8000/')


if __name__ == '__main__':
    for cmd in ['runserver', 'gunserver']:
        t = timeit.Timer('test_runserver()', setup_code.format(cmd=cmd))
        loop, repeat = 1000, 3
        results = t.repeat(repeat, loop)

        print()
        print(cmd, 'loop of', loop, 'repeated', repeat, 'times')
        print('=============')
        print('Average: {mean:.2f}'.format(mean=statistics.mean(results)))
        print('Medians: {me:.2f} {lo:.2f} {hi:.2f}'.format(
            me=statistics.median(results),
            lo=statistics.median_low(results),
            hi=statistics.median_high(results),
        ))
        print('Min/Max: {min:.2f} {max:.2f}'.format(
            min=min(results),
            max=max(results),
        ))
    print()
