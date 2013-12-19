#!/usr/bin/env python
from threading import Thread
from websocket import create_connection
import time, json, pprint

class blockchain_subscriber(Thread):
    def __init__(self, utx_cb=None, block_cb=None):
        Thread.__init__(self)
        self.utx_cb = utx_cb;   
        self.block_cb = block_cb;   
        self.ws = create_connection("ws://ws.blockchain.info/inv")
        self.ws.send( '{"op":"blocks_sub"}');
        self.ws.send( '{"op":"unconfirmed_sub"}');
        self.finished = False;
        self.start();    

    def run(self):
        while not self.finished:
            result = self.ws.recv();
            r = json.loads(result);

            self.utx_cb(r);
            pprint.pprint(r);
 
if __name__ == "__main__":
    def printer(a):
        pprint.pprint(a);
    bs = blockchain_subscriber(printer);
    bs.join();



