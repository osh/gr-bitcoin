#!/usr/bin/env python
from gnuradio import gr
import pmt

def pdu_arg_add(pdu, k, v):
    meta = pmt.car(pdu);
    data = pmt.cdr(pdu);
    if(pmt.is_null(meta)):
        meta = pmt.make_dict();
    assert(pmt.is_dict(meta));
    meta = pmt.dict_add(meta, k, v);
    return pmt.cons(meta,data);

class burst_scheduler(gr.sync_block):
    def __init__(self, feedback_delay = 2048, slot_len = 1000, min_gap = 100):
        gr.sync_block.__init__(
            self, name="blockchain_source",
            in_sig=None, out_sig=None)

        # set up some constants
        self.feedback_delay = feedback_delay;
        self.slot_length = slot_len;
        self.min_gap = min_gap;
        self.nproduced_val = 0;

        # register message i/o
        self.message_port_register_in(pmt.intern("schedule_pdu"));
        self.message_port_register_in(pmt.intern("nproduced"));
        self.message_port_register_out(pmt.intern("scheduled_pdu"))
        self.set_msg_handler(pmt.intern("schedule_pdu"), self.sched_pdu);
        self.set_msg_handler(pmt.intern("nproduced"), self.nproduced);

    def sched_pdu(self, pdu):
        # always schedule on a multiple of slot_length (because we can?)
        sched_time = int((self.nproduced_val + self.min_gap)/self.slot_length)*self.slot_length;
        pdu = pdu_arg_add(pdu, pmt.intern("event_time"), pmt.from_uint64(sched_time));
        self.nproduced_val = self.nproduced_val + len(pmt.c32vector_elements(pmt.cdr(pdu)));
        self.message_port_pub(pmt.intern("scheduled_pdu"), pdu);

    def nproduced(self, produced_pmt):
        nproduced = pmt.to_uint64(produced_pmt);
        self.nproduced_val = max(nproduced+self.feedback_delay, self.nproduced_val);

    
