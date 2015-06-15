#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Compute F-measure

Usage:
    python evaluate.py <prediction> --answer <original_file>

Input:
* KyTea full input format
"""

import argparse
import logging

verbose = False
logger = None

def init_logger():
    global logger
    logger = logging.getLogger('Evaluate')
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)

def main(args):
    global verbose
    verbose = args.verbose

    f1 = 0.0
    N = 0
    with open(args.prediction) as prediction:
        answer = open(args.answer)
        for pred_line in prediction:
            ans_line = answer.readline().strip()
            pred_sep = map(lambda t: t.split('/')[0], pred_line.split())
            ans_sep = map(lambda t: t.split('/')[0], ans_line.split())
            pred = map(lambda t: t.split('/')[1], pred_line.split())
            ans = map(lambda t: t.split('/')[1], ans_line.split())

            match = 0
            ans_pos = 0
            pred_pos = 0
            ans_idx = 0
            pred_idx = 0
            while (ans_idx < len(ans)) and (pred_idx < len(pred)):
                if ans_pos != pred_pos:
                    if ans_pos < pred_pos:
                        ans_pos += len(ans_sep[ans_idx])
                        ans_idx += 1
                    if pred_pos < ans_pos:
                        pred_pos += len(pred_sep[pred_idx])
                        pred_idx += 1
                    continue
                if ans[ans_idx] == pred[pred_idx]:
                    match += 1
                ans_pos += len(ans_sep[ans_idx])
                pred_pos += len(pred_sep[pred_idx])
                ans_idx += 1
                pred_idx += 1
            recall = match / float(len(ans))
            precision = match / float(len(pred))
            try:
                f1 += (2 * recall * precision) / (recall + precision)
            except ZeroDivisionError:
                pass
            N += 1
        answer.close()

    print(f1/float(N))

    return 0


if __name__ == '__main__':
    init_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument('prediction')
    parser.add_argument('--answer', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()
    main(args)
    

