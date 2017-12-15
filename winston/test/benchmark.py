#!/usr/bin/env python3

'''
' test/main.py
'
' Run a series of benchmarks comparing Levenshtein song-matching
' method to syntax-based method.
'
' Will Badart <wbadart@live.com>
' created: DEC 2017
'''

import logging
from collections import defaultdict
from functools import partial, wraps
from itertools import product
from operator import itemgetter
from pickle import dump
from queue import Queue
from random import shuffle
from threading import Lock, Thread
from time import time
from .util import DummySocket
from ..server.util import Command
from ..services.music import Service as Music

LOCK = Lock()
N_THREADS = 8
PICKLE_PATH = '/tmp/benchmark.pickle'
workqueue = Queue()
RESULTS = defaultdict(partial(defaultdict, list))
TEST_SIZE = 120

FORMATS = [
    'play {title}',
    'play {title} by {artist}',
    'play {title} on {album}',
    'play {title} by {artist} on {album}',
    'play {title} on {album} by {artist}',
    'play the song {title}',
    'play the song {title} by {artist}',
    'play the song {title} on {album}',
    'play the song {title} by {artist} on {album}',
    'play the song {title} on {album} by {artist}',
]


def identity(e):
    '''Return arguemtn.'''
    return e


def flatten(a):
    '''Reduce dimensionality of a by one.'''
    return (e for l in a for e in l)


def mkcommand(fmt, song):
    '''Generate a test case given a Song.'''
    cmd_str = fmt.format(**song._asdict())
    return Command(cmd_str)


def timer(f):
    '''Time the execution of f.'''
    @wraps(f)
    def _impl(*args, **kwargs):
        t_start = time()
        result = f(*args, **kwargs)
        return time() - t_start, result
    return _impl


def avg(seq):
    '''Give the mean of a sequence.'''
    return sum(seq) / float(len(seq))


def get_acc(label, result):
    '''Return the numerator and denominator of label's guesses.'''
    label_results = list(flatten(map(itemgetter(label), result.values())))
    hits = sum(1 for t, hit in label_results if hit)
    return hits, len(label_results)


def work():
    '''Wrap the work done for each test case.'''
    while True:
        e = workqueue.get()
        if e is None:
            break
        fmt, (label, method), expected = e
        cmd = mkcommand(fmt, expected)
        t_elapsed, guess = timer(method)(cmd)
        with LOCK:
            RESULTS[fmt][label].append((t_elapsed, guess == expected))
        workqueue.task_done()


def form_results(result_list):
    '''Put the list of results into a nicer data structure.'''
    return result_list


def main():
    '''Execute tests.'''
    logging.info('Starting benchmarks...')

    m = Music(DummySocket(), {})
    listing = list(m.gen_index())
    shuffle(listing)

    methods = {
        'levenshtein': m._guess_old,
        'syntax-base': m._guess,
    }

    threads = []
    for i in range(N_THREADS):
        threads.append(Thread(target=work))
        threads[-1].start()

    for e in product(
            FORMATS, methods.items(), listing[:TEST_SIZE]):
        workqueue.put(e)
    workqueue.join()
    for i in range(N_THREADS):
        workqueue.put(None)
    for t in threads:
        t.join()

    from pprint import pprint
    pprint(RESULTS)
    logging.info('Done.')

    for label in methods:
        print('%s: %d / %d' % (label, *get_acc(label, RESULTS)))

    with open(PICKLE_PATH, 'wb') as fs:
        dump(RESULTS, fs)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(module)s][%(levelname)s]: %(message)s')
    main()
