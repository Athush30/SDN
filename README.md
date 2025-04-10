
# SDN Project with POX Controller and Mininet Topology

This project demonstrates Software-Defined Networking (SDN) using the POX controller and Mininet to create and manage network topologies. It showcases dynamic management of network flows, ARP handling, and forwarding based on learned MAC addresses, all controlled by a POX-based SDN controller.

## Features

- **POX Controller**:
  - Implements a basic learning switch with ARP handling.
  - Dynamically updates IP-to-MAC mappings for accurate forwarding.
  - Adds flow entries to forward packets based on Ethernet type and MAC addresses.

- **Mininet Topology**:
  - Custom topology with two switches and four hosts.
  - Hosts communicate over a shared network, with switches forwarding traffic.
  - Link bandwidth management to simulate realistic network conditions.

- **SDN Concepts**:
  - Centralized control plane with POX managing the data plane.
  - Real-time updates to network flow entries.
  - Dynamic handling of ARP requests and replies for IP-to-MAC mapping.

## Installation

To set up the environment and run this project, follow these steps:

### Prerequisites

- Python 3.6 or higher
- Mininet
- POX controller (with SDN capabilities)
  
### Install Requirements

Create a virtual environment (optional) and install the required dependencies:

```bash
# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Project

1. Start the POX controller:
   ```bash
   ./pox.py controller
   ```
   
2. Run the Mininet topology script:
   ```bash
   sudo python topo.py
   ```

3. Access the Mininet CLI to interact with the network:
   ```bash
   mininet> pingall
   ```

## Networking Skills Demonstrated

- **SDN Fundamentals**:
  - Understanding of centralized control vs. traditional distributed networking.
  - Handling dynamic flow control and ARP mapping.
  
- **Mininet and POX**:
  - Experience with creating custom topologies using Mininet.
  - Configuring and interacting with SDN controllers using POX.
  
- **Network Forwarding and ARP Handling**:
  - Using POX to learn MAC addresses and update flows.
  - Handling ARP requests and replies dynamically to manage IP-to-MAC mappings.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
