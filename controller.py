from pox.core import core
from pox.lib.packet import ethernet, arp
from pox.forwarding.l2_learning import LearningSwitch
from pox.openflow import ofp
import logging

log = core.getLogger()

# === Set up file logging ===
file_handler = logging.FileHandler("pox_controller.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Avoid duplicate log handlers
if not any(isinstance(h, logging.FileHandler) for h in log.handlers):
    log.addHandler(file_handler)

# === Global dictionary to store IP-to-MAC mappings ===
ip_mac_mapping = {}

class SimpleForwarding(LearningSwitch):
    def __init__(self, connection):
        LearningSwitch.__init__(self, connection, False)
        self.connection = connection

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet:
            return

        if packet.type == ethernet.ARP_TYPE:
            self._handle_arp(packet, event.connection)
        else:
            # For other packets, check if a flow exists, otherwise forward normally
            self._add_flow_entry(packet, event)

        # Continue with basic forwarding
        super(SimpleForwarding, self)._handle_PacketIn(event)

    def _handle_arp(self, packet, connection):
        """Handle ARP requests and responses."""
        arp_packet = packet.payload
        if arp_packet.opcode == arp.REQUEST:
            log.debug("ARP Request: %s is asking about %s",
                      arp_packet.hwsrc, arp_packet.protosrc)

        elif arp_packet.opcode == arp.REPLY:
            log.debug("ARP Reply: %s has IP %s",
                      arp_packet.hwsrc, arp_packet.protosrc)

            current_mac = arp_packet.hwsrc
            ip = arp_packet.protosrc

            if ip not in ip_mac_mapping:
                ip_mac_mapping[ip] = current_mac
                log.info("Mapped IP %s to MAC %s", ip, current_mac)
            elif ip_mac_mapping[ip] != current_mac:
                old_mac = ip_mac_mapping[ip]
                ip_mac_mapping[ip] = current_mac
                log.warning("Updated: IP %s changed from MAC %s to %s", ip, old_mac, current_mac)

        # Add flow entry for ARP responses (to avoid reprocessing ARP)
        self._add_flow_entry(packet, connection)

    def _add_flow_entry(self, packet, connection):
        """Add a flow entry to the switch."""
        msg = ofp.ofp_flow_mod()
        msg.priority = 1  # Set a lower priority for general forwarding (ARP and data packets)
        
        # Set match criteria
        match = ofp.ofp_match()
        match.dl_src = packet.src  # Match source MAC address
        match.dl_dst = packet.dst  # Match destination MAC address
        match.dl_type = packet.type  # Match Ethernet type (e.g., ARP, IP)

        # Set actions (forward the packet to the output port)
        action = ofp.ofp_action_output(port=connection.ofp_port)
        msg.actions.append(action)

        msg.match = match

        # Add flow entry
        connection.send(msg)
        log.info("Flow entry added for packet: src=%s, dst=%s", packet.src, packet.dst)

def list_ip_mac_mappings():
    """List all stored IP-to-MAC mappings."""
    log.debug("=== IP-to-MAC Mappings ===")
    for ip, mac in ip_mac_mapping.items():
        log.debug("IP Address: %s, MAC Address: %s", ip, mac)

def start_switch(event):
    log.debug("Switch connected: %s", event.connection)
    SimpleForwarding(event.connection)
    list_ip_mac_mappings()

def launch():
    log.debug("POX controller initialized and listening for switches...")
    core.openflow.addListenerByName("ConnectionUp", start_switch)
