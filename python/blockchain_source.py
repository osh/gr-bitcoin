#!/usr/bin/env python

from gnuradio import gr,blocks
from blockchain_subscriber import *
import pmt,json

class blockchain_source(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self, name="blockchain_source",
            in_sig=None, out_sig=None)

        self.message_port_register_out(pmt.intern("utx"))
        self.message_port_register_out(pmt.intern("block"))

    def start(self):
        self.bs = blockchain_subscriber(self.utx,self.blk);
    
    def stop():
        self.bs.stop();

    def utx(self, arg):
        self.message_port_pub(pmt.intern("utx"), 
                              pmt.intern(json.dumps(arg)));

    def blk(self, arg):
        self.message_port_pub(pmt.intern("block"), 
                              pmt.intern(json.dumps(arg)));
 
if __name__ == "__main__":
    tb = gr.top_block();
    src = blockchain_source();
    snk = blocks.message_debug();
    tb.msg_connect( src,"utx", snk,"print" );
    tb.run();
   
