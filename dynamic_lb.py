from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
from ryu.lib import hub

class DynamicLoadBalancer(app_manager.RyuApp):
    OFP_VERSION = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(DynamicLoadBalancer, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths = {}
        self.port_stats = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange, CONFIG_DISPATCHER)
    def state_change(self, ev):
        datapath = ev.datapath
        if datapath.id not in self.datapaths:
            self.datapaths[datapath.id] = datapath

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                ofproto = dp.ofproto
                parser = dp.ofproto_parser
                req = parser.OFPPortStatsRequest(dp, 0, ofproto.OFPP_ANY)
                dp.send_msg(req)
            hub.sleep(3)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def port_stats_reply(self, ev):
        dp = ev.msg.datapath
        dpid = dp.id
        self.port_stats[dpid] = {}
        for stat in ev.msg.body:
            self.port_stats[dpid][stat.port_no] = stat.tx_bytes

    def add_flow(self, dp, priority, match, actions):
        ofproto = dp.ofproto
        parser = dp.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=dp, priority=priority, match=match, instructions=inst)
        dp.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        dpid = dp.id
        parser = dp.ofproto_parser
        ofproto = dp.ofproto

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth.ethertype == 35020:
            return

        dst = eth.dst
        src = eth.src
        in_port = msg.match['in_port']

        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        if dpid in self.port_stats:
            try:
                out_port = min(self.port_stats[dpid], key=self.port_stats[dpid].get)
            except:
                pass

        actions = [parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
        self.add_flow(dp, 1, match, actions)

        out = parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions)
        dp.send_msg(out)
