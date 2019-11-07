"""
    Copyright 2019 Tae-Hwan Jung
    MIT LICENSE
    code reference : https://soooprmx.com/archives/6436,
        https://github.com/google-research/bert/blob/master/create_pretraining_data.py

    ventilator for masked language model preprocessing pipeline
    This code must be executed after wikiextractor script has been **finished**.
    `data` : dump data root folder path, it has to seems like below:
    `vserver` : ventilator server
    `vport` : number of ventilator port
    `sserver` : sink server
    `sport` : number of sink port
"""
import sys
import zmq
import argparse
from bs4 import BeautifulSoup

ctx = zmq.Context()

def main(args):
    server_pull, server_push = args.vserver, args.sserver
    port_pull, port_push = args.vport, args.sport

    sock_pull = ctx.socket(zmq.PULL)
    sock_pull.connect(f'tcp://{server_pull}:{port_pull}')

    sock_push = ctx.socket(zmq.PUSH)
    sock_push.connect(f'tcp://{server_push}:{port_push}')

    while True:
        data = sock_pull.recv_string()

        bs = BeautifulSoup(data, 'html.parser')
        block = ''
        for doc in bs.find('doc'):
            block += doc
        sys.stdout.flush()

        res = block # TODO res = f(data)
        sock_push.send_string(res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='worker for masked '
                                                 'language model preprocessing pipeline')
    parser.add_argument('--vserver', type=str, default='127.0.0.1', help='ventilator server')
    parser.add_argument('--vport', type=int, default=5557, help='ventilator port')
    parser.add_argument('--sserver', type=str, default='127.0.0.1', help='sink server')
    parser.add_argument('--sport', type=int, default=5556, help='sink port')
    args = parser.parse_args()

    main(args=args)
