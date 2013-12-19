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

    def stop(self):
        self.finished = True;

    def run(self):
        while not self.finished:
            result = self.ws.recv();
            r = json.loads(result);
            if(r["op"]=="utx" and self.utx_cb):
                self.utx_cb(r);
            elif(self.block_cb):
                self.block_cb(r);
 
if __name__ == "__main__":
    def printer(a):
        pprint.pprint(a);
    bs = blockchain_subscriber(printer,printer);
    bs.join();

