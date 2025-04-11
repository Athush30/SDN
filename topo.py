from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController

# Define a custom topology by subclassing Topo
class CustomTopo(Topo):
    def build(self):
        # Create switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        
        # Create hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        
        # Add links between hosts and switches
        self.addLink(h1, s1, bw=10)  # Host h1 to switch s1
        self.addLink(h2, s1, bw=10)  # Host h2 to switch s1
        self.addLink(h3, s2, bw=10)  # Host h3 to switch s2
        self.addLink(h4, s2, bw=10)  # Host h4 to switch s2
        
        # Add a link between switches (s1 and s2)
        self.addLink(s1, s2, bw=20)  # Link between s1 and s2

# Create the network based on the custom topology
topo = CustomTopo()
net = Mininet(topo=topo, controller=RemoteController)
net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

# Start the network
net.start()

# Run Mininet CLI for interaction
CLI(net)

# Stop the network after using the CLI
net.stop()
