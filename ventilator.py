"""
    Copyright 2019 Tae-Hwan Jung
    MIT LICENSE
    code reference : https://soooprmx.com/archives/6436

    ventilator for masked language model preprocessing pipeline
    This code must be executed after wikiextractor script has been **finished**.
    `data` : dump data root folder path, it has to seems like below:
    `vport` : number of ventilator port
    `sport` : number of sink port
"""
import os
import sys
import uuid
import random
import zmq
import argparse
from pathlib import Path

ctx = zmq.Context()

def main(args):
    sock = ctx.socket(zmq.PUSH)
    sock.bind(f'tcp://*:{args.vport}')

    cmd = ctx.socket(zmq.PUSH)
    cmd.connect(f'tcp://{args.sserver}:{args.sport}')

    files = []
    for filename in Path(args.data).rglob('*'):
        if os.path.isfile(filename):
            files.append(filename) # 100(0~99) * 26(A-Z) * 26(A-Z)

    # send total number of files to `sink`
    cmd.send(len(files).to_bytes(8, 'big'))

    print(f"START VENT SERVER")
    input("> IF YOU'RE READY, PRESS ENTER TO START")
    print('%d files....' % (len(files)))

    for file in files:
        with open(file, 'r') as f:
            sock.send_json({
                'key' : str(uuid.uuid4()),
                'text' : f.read()
            })

    input("PRESS ENTER TO QUIT")
    ctx.destroy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ventilator for masked '
                                                 'language model preprocessing pipeline')
    parser.add_argument('--data', type=str, default='./data')
    parser.add_argument('--vport', type=int, default=5557, help='ventilator port')
    parser.add_argument('--sserver', type=str, default='127.0.0.1', help='sink server')
    parser.add_argument('--sport', type=int, default=5556, help='sink port')
    args = parser.parse_args()

    main(args=args)