#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""Predict words given a series of first-two-characters
"""
import argparse
import logging
import pickle
import numpy as np

verbose = False
logger = None

N = 0
l1 = 0
l2 = 0
prior = {}
transition = {}
emit = {}
possible_words = {}

def init_logger():
    global logger
    logger = logging.getLogger('Test')
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)

def smooth_prior(word):
    return l1 * prior.get(word, 0.0) / float(N) + (1 - l1) / float(N)

def smooth_transition(prev_word, next_word):
    return l2 * transition.get((prev_word, next_word), 0.0) \
           + (1 - l2) * smooth_prior(next_word)

def forward(line):
    words = [line[i:i+2] for i in range(0, len(line), 2)]
    best_score = {}
    best_edge = {}
    best_score[(0, '<s>')] = 0
    best_edge[(0, '<s>')] = None
    prev_word = '<s>'
    possible_prev_words = ['<s>',]
    possible_next_words = []
    for i in xrange(len(words)):
        try:
            possible_next_words = possible_words[words[i][:2]]
        except KeyError:  # word[i] = unknown word
            possible_next_words = []
            for prev_word in possible_prev_words:
                label = 'UNKNOWN_'+prev_word
                best_edge[(i+1, label)] = (i, prev_word)
                possible_next_words.append(label)
            possible_prev_words = possible_next_words
            continue

        for prev_word in possible_prev_words:
            if prev_word.split('_')[0] == 'UNKNOWN':
                for next_word in possible_next_words:
                    score = best_score[(i-1, prev_word.split('_')[1])]
                    best_score[(i+1, next_word)] = score
                    best_edge[(i+1, next_word)] = (i, prev_word)
                continue

            for next_word in possible_next_words:
                if best_score.get((i, prev_word)) is not None:
                    score = best_score[(i, prev_word)] \
                            - np.log(smooth_transition(prev_word, next_word))
                    if (best_score.get((i+1, next_word)) is None) \
                       or (best_score.get((i+1, next_word)) > score):
                        best_score[(i+1, next_word)] = score
                        best_edge[(i+1, next_word)] = (i, prev_word)
        possible_prev_words = possible_next_words
    i = len(words)
    for prev_word in possible_prev_words:
        if best_score.get((i, prev_word)):
            score = best_score[(len(words), prev_word)] \
                    - np.log(smooth_transition(prev_word, '<eos>'))
            if (best_score.get((i+1, '<eos>'), score+1) >= score):
                best_score[(i+1, '<eos>')] = score
                best_edge[(i+1, '<eos>')] = (i, prev_word)
    return best_score, best_edge

def backward(best_edge, L):
    words = []
    next_edge = best_edge[(L, '<eos>')]
    while next_edge != (0, '<s>'):
        words.append(next_edge[1])
        next_edge = best_edge[next_edge]

    return map(lambda x: x.strip(), words[::-1])


def main(args):
    global prior, N, l1, l2, transition, possible_words
    global verbose
    verbose = args.verbose
    if verbose: logger.info('Load model {}'.format(args.model))
    with open(args.model, 'rb') as f:
        data = pickle.load(f)
        prior = data['prior']
        transition = data['transition']
        # emit = data['emit']

    possible_words = {}
    for key in prior.keys():
        try:
            possible_words[key[:2]].append(key)
        except KeyError:
            possible_words[key[:2]] = [key,]

    N = sum(prior.values())
    l1 = args.l1
    l2 = args.l2
    # for key in transition.keys():
    #     transition[key] /= float(prior[key[0]])


    fout = open(args.output, 'w')
    with open(args.filename) as f:
        for line in f:
            words = line.strip().split()
            l = []
            for word in words:
                c = word.split('/')[0]
                if len(c) == 1: c += ' '
                l.append(c)
            x = ''.join(l)
            best_score, best_edge = forward(x)
            y = backward(best_edge, len(words)+1)
            pairs = ['{}/{}/blank'.format(words[i].split('/')[0], y[i])
                     for i in range(len(y))]
            fout.write(' '.join(pairs))
            fout.write('\n')
            if verbose: logger.info(' '.join(pairs))
    fout.close()
    return 0

if __name__ == '__main__':
    init_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-o', '--output', action='store', default='out')
    parser.add_argument('--model', action='store', default='model')
    parser.add_argument('--l1', action='store', type=float, default=0.8)
    parser.add_argument('--l2', action='store', type=float, default=0.8)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()
    main(args)
