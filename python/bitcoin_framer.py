#!/usr/bin/env python

from gnuradio import gr,blocks
import pmt, bitarray

class framer(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self, name="blockchain_source",
            in_sig=None, out_sig=None)

        self.header = "SATOSHIWIRELESS";
        self.message_port_register_in(pmt.intern("msg_string"));
        self.message_port_register_out(pmt.intern("pdu"))
        self.set_msg_handler(pmt.intern("msg_string"), self.handle_msg);

    def handle_msg(self, arg):
        msg = pmt.write_string(arg);
        fullmsg = self.header + msg;
        ba = bitarray.bitarray();
        ba.fromstring(fullmsg);
        fsl = ba.tolist();
        pdu = pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(len(fsl), fsl));
#        pdu = pmt.cons(pmt.PMT_NIL,pmt.to_pmt(map(lambda x: int(x), ba.tolist())));
        self.message_port_pub(pmt.intern("pdu"), pdu);
        #print pdu;

 
