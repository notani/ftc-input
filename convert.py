#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Convert raw texts into KyTea format

Usage:
    python convert.py <raw_text.gz> -v > <output>
"""

import argparse
import logging
import gzip

verbose = False
logger = None

def init_logger():
    global logger
    logger = logging.getLogger('Converter')
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)

def main(args):
    global verbose
    verbose = args.verbose

    with gzip.open(args.filename) as f:
        for i, line in enumerate(f):
            l = line.decode('utf8').split()
            out = []
            for w in l:
                w = w.replace('/', '|')  # replaced / with |
                out.append(u'{}/{}/blank'.format(w[:2],w))
            print(u' '.join(out).encode('utf8'))
            if verbose and (i+1) % 1000 == 0:
                logger.info('{} line'.format(i))
    return 0

if __name__ == '__main__':
    init_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()
    main(args)
    

