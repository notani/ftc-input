#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Train a model
"""

import argparse
import logging
import pickle

verbose = False
logger = None

def init_logger():
    global logger
    logger = logging.getLogger('Train')
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)

def main(args):
    global verbose
    verbose = args.verbose
    prior = {}
    transition = {}
    with open(args.filename) as f:
        for line in f:
            previous = '<s>'
            words = line.split()
            for word in words:
                t = word.split('/')
                if len(t[0]) == 1:
                    t[0] += ' '
                    t[1] += ' '
                try:
                    prior[previous] += 1
                except KeyError:
                    prior[previous] = 1
                try:
                    transition[(previous, t[1])] += 1
                except KeyError:
                    transition[(previous, t[1])] = 1
                previous = t[1]
            try:
                prior[previous] += 1
            except KeyError:
                prior[previous] = 1
            try:
                transition[(previous, '<eos>')] += 1
            except KeyError:
                transition[(previous, '<eos>')] = 1

    if verbose: logger.info('Normalize transition probability')
    for key in transition.keys():
        transition[key] /= float(prior[key[0]])
    if verbose: logger.info('Save model {}'.format(args.model))
    with open(args.model, 'wb') as f:
        pickle.dump({'prior': prior,
                     'transition': transition}, f)

    return 0

if __name__ == '__main__':
    init_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--model', action='store', default='model')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()
    main(args)
