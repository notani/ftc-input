#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Convert KyTea format texts into raw texts

Usage:
    python prepare_kytea_test.py <source> > <destination>
"""

import argparse
import logging

verbose = False
logger = None

def init_logger():
    global logger
    logger = logging.getLogger('ConvertIntoRaw')
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)

def main(args):
    global verbose
    verbose = args.verbose

    with open(args.filename) as f:
        for i, line in enumerate(f):
            l = line.decode('utf8').split()
            out = []
            for i in range(len(l)):
                try:
                    out.append(l[i].split('/')[0].strip())
                except IndexError:
                    out.append(l[i].split('/')[0].strip())
                    i += 1
            print(u''.join(out).encode('utf8'))
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
    

