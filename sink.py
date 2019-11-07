"""
    Copyright 2019 Tae-Hwan Jung
    MIT LICENSE
        code reference : https://soooprmx.com/archives/6436


    sink for masked language model preprocessing pipeline
    This code must be executed after wikiextractor script has been **finished**.
"""

import zmq
import sys
import argparse

ctx = zmq.Context()

def main(args):
    sock = ctx.socket(zmq.PULL)
    sock.bind("tcp://*:%d" % (args.sport))

    print("STARTING SERVER AT %d" % (args.sport))

    sig_start = sock.recv()
    v = int.from_bytes(sig_start, 'big')
    print("GATHER %d TASKS." % (v))
    cnt = 0

    for task_no in range(v):
        data = sock.recv_string()
        print(data)
        if data == 'DONE':
            cnt += 1
            print("%d/%d(%.2f) TASKS WAS DONE" % (cnt, v, (cnt / v) * 100))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sink for masked '
                                                 'language model preprocessing pipeline')


    parser.add_argument('--sport', type=int, default=5556, help='sink port')
    args = parser.parse_args()
    main(args=args)
